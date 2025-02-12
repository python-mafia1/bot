import asyncio

from livekit import rtc


async def do_something(track: rtc.RemoteAudioTrack):
    audio_stream = rtc.AudioStream(track)
    async for event in audio_stream:
        # Do something here to process event.frame
        pass
    await audio_stream.aclose()


async def entrypoint(ctx: JobContext):
  # connect to the room
  await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

  # wait for the first participant to arrive
  participant = await ctx.wait_for_participant()

  # customize behavior based on the participant
  print(f"connected to room {ctx.room.name} with participant {participant.identity}")

  # inspect the current value of the attribute
  language = participant.attributes.get("user.language")

  # listen to when the attribute is changed
  @ctx.room.on("participant_attributes_changed")
  def on_participant_attributes_changed(changed_attrs: dict[str, str], p: rtc.Participant):
      if p == participant:
        language = p.attributes.get("user.language")
        print(f"participant {p.identity} changed language to {language}")