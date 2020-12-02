"""Manage tasks for the advent 2020 challenge package."""
import tempfile
from typing import Any

import nox
from nox.sessions import Session

package: str = "advent"
nox.options.sessions = "safety", "black", "lint", "mypy", "tests"
locations = "src", "tests", "noxfile.py"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Parameters
    ----------
    session: Session
        The Session object.
    args: str
        Command-line arguments for pip.
    kwargs: Any
        Additional keyword arguments for Session.install.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python="3.9")
def black(session):
    """Run black code formatter.

    Parameters
    ----------
    session: Session
        The Session object.
    """
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.9")
def lint(session):
    """Lint using flake8.

    Parameters
    ----------
    session: Session
        The Session object.
    """
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "flake8-annotations",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python="3.9")
def mypy(session):
    """Check type annotations using mypy.

    Parameters
    ----------
    session: Session
        the Session object
    """
    args = session.posargs or locations
    # session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python="3.9")
def safety(session):
    """Scan dependencies for insecure packages.

    Parameters
    ----------
    session: Session
        The Session object.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python="3.9")
def tests(session):
    """Run the test suite.

    Parameters
    ----------
    session: Session
        The Session object.
    """
    args = session.posargs or []
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest")
    session.run("pytest", *args)
