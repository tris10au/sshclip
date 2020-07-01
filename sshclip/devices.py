import paramiko
import pathlib
import socket
import time
import os
import io

class BaseDevice(object):
    NAME = "ABSTRACT"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def read(self, filename):
        raise NotImplementedError

    def stat(self, filename):
        raise NotImplementedError

    def write(self, filename, value):
        raise NotImplementedError

    def find_clip_path(self):
        raise NotImplementedError


class ClientDevice(BaseDevice):
    NAME = "CLIENT"

    _connection = None
    _sftp = None
    _username = None

    def parse_host(self, host_str):
        username = None
        port = 22

        if "@" in host_str:
            username, host_str = host_str.split("@", 1)

        if ":" in host_str:
            host_str, port = host_str.split(":")
            port = int(port)

        return (host_str, port, username)

    def get_host_key_file(self):
        path = os.path.expanduser("~/.ssh/known_hosts")

        if not os.path.exists(path):
            path = os.path.expanduser("~/ssh/known_hosts")
        
        return path

    def __init__(self, host_str):
        host, port, self._username = self.parse_host(host_str)
        self._connection = paramiko.SSHClient()
        self._connection.get_host_keys().load(self.get_host_key_file())
        self._connection.connect(host, username=self._username, port=port)
        self._sftp = self._connection.open_sftp()

    def __exit__(self, exc_type, exc_value, tb):
        if self._connection is not None:
            self._connection.close()

    def read(self, filename):
        with self._sftp.open(filename, "r") as file:
            return file.read().decode("utf-8")

    def write(self, filename, value):
        print("WRITING: ", filename, value)
        with self._sftp.open(filename + ".tmp", "w") as file:
            file.write(value.encode("utf-8"))
        self._sftp.posix_rename(filename + ".tmp", filename)

    def stat(self, filename):
        return self._sftp.lstat(filename)

    def find_clip_path(self):
        if self._username is not None:
            if self._username == "root":
                return "/root/.ssh_clip"
            else:
                return "/home/{username}/.ssh_clip".format(username=self._username)
        else:
            return "/tmp/.ssh_clip"


class ServerDevice(BaseDevice):
    NAME = "SERVER"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def read(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    def write(self, filename, value):
        with open(filename + ".tmp", "w", encoding="utf-8") as file:
            file.write(value)
        os.rename(filename + ".tmp", filename)

    def stat(self, filename):
        return os.lstat(filename)

    def find_clip_path(self):
        return os.path.expanduser("~/.ssh_clip")
