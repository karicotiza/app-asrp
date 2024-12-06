"""Speech recognition algorithm."""

from src.placeholders import some_bytes, some_int, some_logic, some_string


class AudioEntity:
    """Audio entity."""

    def __init__(self, audio_data: bytes) -> None:
        """Make new instance.

        Args:
            audio_data (bytes): bytes of audio.
        """
        self._audio_data: bytes = audio_data

    @property
    def audio_data(self) -> bytes:
        """Get audio data.

        Returns:
            bytes: bytes of audio.
        """
        return self._audio_data


class IdentifierEntity:
    """Identifier entity."""

    def __init__(self) -> None:
        """Make new instance."""
        self._id: str = self._create_uuid()

    @property
    def id(self) -> str:
        """Get identifier value.

        Returns:
            str: identifier value.
        """
        return self._id

    def _create_uuid(self) -> str:
        return some_string


class TranscriptionEntity:
    """Transcription entity."""

    def __init__(
        self,
        start: int,
        end: int,
        text: str,
    ):
        """Make new instance.

        Args:
            start (int): start of transcription in audio.
            end (int): end of transcription in audio.
            text (str): text of the transcription.
        """
        self._start: int = start
        self._end: int = end
        self._text: str = text

    @property
    def start(self) -> int:
        """Transcription start time in milliseconds.

        Returns:
            int: start time in milliseconds
        """
        return self._start

    @property
    def end(self) -> int:
        """Transcription end time in milliseconds.

        Returns:
            int: end time in milliseconds
        """
        return self._end

    @property
    def text(self) -> str:
        """Transcription text.

        Returns:
            str: text.
        """
        return self._text


class AudioQueueService:
    """Audio queue service."""

    def __init__(self) -> None:
        """Make new instance."""
        self._audio_queue: bytes = some_bytes

    async def dequeue(self, duration_in_milliseconds: int) -> AudioEntity:
        """Dequeue (get and delete from the beginning) audio entity.

        Args:
            duration_in_milliseconds (int): chunk duration.

        Returns:
            AudioEntity: audio entity, if there is left any.
        """
        return AudioEntity(some_bytes)

    async def enqueue(self, audio: AudioEntity) -> None:
        """Enqueue (append to the end) audio entity.

        Args:
            audio (AudioEntity): audio entity.
        """
        self._audio_queue += audio.audio_data

    async def not_empty(self) -> bool:
        """Check if queue not empty.

        Returns:
            bool: true if not empty
        """
        return bool(self._audio_queue)


class TranscriptionQueueService:
    """Transcription queue service."""

    def __init__(self) -> None:
        """Make new instance."""
        self._transcription_queue: list[TranscriptionEntity] = []

    async def dequeue(self) -> list[TranscriptionEntity]:
        """Dequeue (get and delete from the beginning) transcription entities.

        Returns:
            AudioEntity: audio entity, if there is left any.
        """
        memory: list[TranscriptionEntity] = []

        while self._transcription_queue:
            memory.append(self._transcription_queue.pop())

        return memory

    async def enqueue(self, transcriptions: list[TranscriptionEntity]) -> None:
        """Enqueue (append to the end) transcription entity.

        Args:
            transcriptions (list[TranscriptionEntity]): list of transcription \
                entities.
        """
        self._transcription_queue += transcriptions


class AudioRecognitionService:
    """Audio recognition service."""

    async def transcribe(self, audio: AudioEntity) -> str:
        """Get transcription of audio.

        Args:
            audio (AudioEntity): audio entity.

        Returns:
            str: transcription of audio.
        """
        return some_string


class SessionEntity:
    """Session entity."""

    def __init__(self) -> None:
        """Make new instance."""
        self._audio_queue: AudioQueueService = AudioQueueService()
        self._transcription_queue: TranscriptionQueueService = (
            TranscriptionQueueService()
        )

        self._audio_recognition: AudioRecognitionService = (
            AudioRecognitionService()
        )

    @property
    def audio_queue(self) -> AudioQueueService:
        """Get audio queue.

        Returns:
            AudioQueueService: audio queue service.
        """
        return self._audio_queue

    @property
    def transcription_queue(self) -> TranscriptionQueueService:
        """Get transcription queue.

        Returns:
            TranscriptionQueueService: transcription queue service.
        """
        return self._transcription_queue

    async def process(self) -> None:
        """Process audio queue until it's empty."""
        while self._audio_queue.not_empty():
            audio: AudioEntity = await self._audio_queue.dequeue(some_int)
            transcription: TranscriptionEntity = TranscriptionEntity(
                some_int,
                some_int,
                await self._audio_recognition.transcribe(audio),
            )
            await self._transcription_queue.enqueue([transcription])


class SessionRepository:
    """Session repository."""

    async def create(self, identifier: IdentifierEntity) -> None:
        """Create session.

        Args:
            identifier (IdentifierEntity): session identifier entity.
        """
        await some_logic()

    async def read(self, identifier: IdentifierEntity) -> SessionEntity:
        """Read session.

        Args:
            identifier (IdentifierEntity): identifier entity.

        Returns:
            SessionEntity: session entity.
        """
        return SessionEntity()


class CreateSessionUseCase:
    """Upload audio use case."""

    async def command(self) -> IdentifierEntity:
        """Do use case.

        Returns:
            IdentifierEntity: identifier entity.
        """
        identifier: IdentifierEntity = IdentifierEntity()
        await SessionRepository().create(identifier)
        return identifier


class AddAudioToSessionUseCase:
    """Add audio to session use case."""

    async def command(
        self, identifier: IdentifierEntity, audio: AudioEntity,
    ) -> None:
        """Do use case.

        Args:
            identifier (IdentifierEntity): identifier entity.
            audio (AudioEntity): audio entity.
        """
        session: SessionEntity = await SessionRepository().read(identifier)
        await session.audio_queue.enqueue(audio)
        await session.process()


class GetTranscriptionsFromSessionUseCase:
    """Get audio from session use case."""

    async def command(
        self, identifier: IdentifierEntity,
    ) -> list[TranscriptionEntity]:
        """Do use case.

        Args:
            identifier (IdentifierEntity): identifier entity.

        Returns:
            list[TranscriptionEntity]: list of transcription entities.
        """
        session: SessionEntity = await SessionRepository().read(identifier)
        return await session.transcription_queue.dequeue()
