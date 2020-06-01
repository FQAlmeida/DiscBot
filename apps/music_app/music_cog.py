import asyncio

from discord import (opus, InvalidArgument, ClientException, VoiceChannel)
from discord.ext.commands import Cog, command, Context, guild_only


class MusicCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    @staticmethod
    def check_opus():
        if not opus.is_loaded():
            opus.load_opus("dll/opus/libopus-0.dll")
        return opus.is_loaded()

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            # noinspection PyBroadException
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @command()
    @guild_only()
    async def join(self, ctx: Context, channel: VoiceChannel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except InvalidArgument:
            await ctx.send('This is not a voice channel...')
        except ClientException:
            await ctx.send('Already in a voice channel...')
        else:
            await ctx.send('Ready to play audio in ' + channel.name)

    @command()
    @guild_only()
    async def summon(self, ctx: Context):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await ctx.send('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @command()
    @guild_only()
    async def play(self, ctx: Context, *, song: str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await ctx.send(fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await ctx.send('Enqueued ' + str(entry))
            await state.songs.put(entry)

    @command()
    @guild_only()
    async def volume(self, ctx: Context, value: int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    @command()
    @guild_only()
    async def pause(self, ctx: Context):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @command()
    @guild_only()
    async def resume(self, ctx: Context):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @command()
    @guild_only()
    async def stop(self, ctx:Context):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        # noinspection PyBroadException
        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @command()
    @guild_only()
    async def skip(self, ctx: Context):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await ctx.send('Not playing any MusicCog right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await ctx.send('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await ctx.send('Skip vote passed, skipping song...')
                state.skip()
            else:
                await ctx.send('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await ctx.send('You have already voted to skip this song.')

    @command()
    @guild_only()
    async def playing(self, ctx: Context):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await ctx.send('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await ctx.send('Now playing {} [skips: {}/3]'.format(state.current, skip_count))


class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()  # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            # await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()
