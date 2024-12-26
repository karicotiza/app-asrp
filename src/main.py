"""Automatic speech recognition pipeline.

Pseudo-code for universal automatic speech recognition pipeline that can
handle:
* One request with very long audio (e. g. 8 hour audio);
* Infinite amount of requests with small audios (e. g. 1 second of audio every
second).
"""

from typing import Protocol


# Domain
class SessionEntity:
    """Session entity."""

    def __init__(self) -> None:
        """Create new instance."""
        self._data: bytes = b''  # noqa: WPS110
        self._amount_of_processed_audios: int = 0
        self._amount_of_unprocessed_audios: int = 0
        self._transcriptions: list[str] = []

    @property
    def amount_of_processed_audios(self) -> int:
        """Get amount of processed audios.

        Returns:
            int: amount of processed audios.
        """
        return self._amount_of_processed_audios

    @property
    def amount_of_unprocessed_audios(self) -> int:
        """Get amount of unprocessed audios.

        Returns:
            int: amount of unprocessed audios.
        """
        return self._amount_of_unprocessed_audios

    def append_audio(self, audio: bytes) -> None:
        """Append audio to session.

        Args:
            audio (bytes): bytes of audio.
        """
        pass  # noqa: WPS420

    def retrieve_transcriptions(self) -> list[str]:
        """Retrieve transcriptions.

        Returns:
            list[str]: transcriptions.
        """
        return self._transcriptions


class SessionFactory:
    """Session factory."""

    def create(self) -> tuple[int, SessionEntity]:
        """Create pair of pk and session entity.

        Returns:
            tuple[int, SessionEntity]: pk and session entity.
        """
        return (self._create_random_pk(), SessionEntity())

    def _create_random_pk(self) -> int:
        return 0


class SessionRepositoryInterface(Protocol):
    """Session repository interface."""

    def create(self, pk: int, session: SessionEntity) -> None:
        """Abstract creation of a new session.

        Args:
            pk (int): primary key.
            session (SessionEntity): session entity.
        """
        pass  # noqa: WPS420

    def retrieve(self, pk: int) -> SessionEntity:
        """Retrieve session.

        Args:
            pk (int): primary key.
        """
        pass  # noqa: WPS420


# Application
class Worker:
    """Worker (event handler)."""

    def run_in_thread(self) -> None:
        """Run worker in thread."""
        pass  # noqa: WPS420


class CreateSessionUseCase:
    """Create session use case."""

    def execute(self, repository: SessionRepositoryInterface) -> int:
        """Do use case.

        Args:
            repository (SessionRepositoryInterface): any session repository.

        Returns:
            int: primary key of created session entity.
        """
        pk, session = SessionFactory().create()
        repository.create(pk, session)
        return pk


class RetrieveSessionStatisticUseCase:
    """Retrieve session statistics use case."""

    def execute(
        self,
        repository: SessionRepositoryInterface,
        pk: int,
    ) -> tuple[int, int]:
        """Do use case.

        Args:
            repository (SessionRepositoryInterface): any session repository.
            pk (int): primary key.

        Returns:
            tuple[int, int]: amount of processed and unprocessed audios.
        """
        session: SessionEntity = repository.retrieve(pk)

        return (
            session.amount_of_processed_audios,
            session.amount_of_unprocessed_audios,
        )


class AddAudioToSessionUseCase:
    """Add audio to session use case."""

    def execute(
        self,
        repository: SessionRepositoryInterface,
        pk: int,
        audio: bytes,
    ) -> None:
        """Do use case.

        Args:
            repository (SessionRepositoryInterface): any session repository.
            pk (int): primary key.
            audio (bytes): bytes of audio.
        """
        session: SessionEntity = repository.retrieve(pk)
        session.append_audio(audio)


class RetrieveTranscriptionsOfSessionUseCase:
    """Retrieve transcriptions of session."""

    def execute(
        self,
        repository: SessionRepositoryInterface,
        pk: int,
    ) -> list[str]:
        """Do use case.

        Args:
            repository (SessionRepositoryInterface): any session repository.
            pk (int): primary key

        Returns:
            list[str]: transcriptions.
        """
        session: SessionEntity = repository.retrieve(pk)
        return session.retrieve_transcriptions()


# Infrastructure
class SessionRepository:
    """Session repository."""

    _db: dict[int, SessionEntity] = {}

    def create(self, pk: int, session: SessionEntity) -> None:
        """Create new session.

        Args:
            pk (int): primary key.
            session (SessionEntity): session entity.
        """
        self._db[pk] = session

    def retrieve(self, pk: int) -> SessionEntity:
        """Retrieve session.

        Args:
            pk (int): primary key.

        Returns:
            SessionEntity: session entity.
        """
        return self._db[pk]


# User Interface
class Controller:
    """Controller."""

    _session_repository: SessionRepositoryInterface = SessionRepository()

    def create_session(self) -> dict[str, int]:
        """Create (post) session endpoint.

        Returns:
            dict[str, int]: response body.
        """
        return {
            'pk': CreateSessionUseCase().execute(self._session_repository),
        }

    def retrieve_session_statistics(self, pk: int) -> dict[str, int]:
        """Retrieve (get) session statistics.

        Args:
            pk (int): primary key of session entity.

        Returns:
            dict[str, int]: response body
        """
        processed, unprocessed = RetrieveSessionStatisticUseCase().execute(
            self._session_repository, pk,
        )

        return {
            'processed': processed,
            'in_process': unprocessed,
        }

    def add_audio(self, pk: int, audio: bytes) -> dict[str, str]:
        """Add (post) audio to session.

        Args:
            pk (int): primary key of session entity.
            audio (bytes): bytes of audio.

        Returns:
            dict[str, int]: response body
        """
        AddAudioToSessionUseCase().execute(self._session_repository, pk, audio)
        return {'status': 'ok'}

    def retrieve_transcriptions(self, pk: int) -> dict[str, list[str]]:
        """Retrieve (get) transcriptions of session.

        Args:
            pk (int): primary key of session

        Returns:
            dict[str, str]: response body.
        """
        return {
            'transcriptions': RetrieveTranscriptionsOfSessionUseCase().execute(
                self._session_repository, pk,
            ),
        }


if __name__ == '__main__':
    controller: Controller = Controller()
    worker: Worker = Worker()
    worker.run_in_thread()
