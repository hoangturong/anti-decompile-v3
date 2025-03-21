import sys
import os
import ctypes
import threading
import time
import random
import marshal
import base64
import zlib
import dis
import types
import inspect
import binascii
import hashlib
import signal
import struct
import platform
import subprocess
import logging
import builtins
import opcode
import atexit
from functools import wraps
from contextlib import suppress
from abc import ABC, abstractmethod
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# High-level encryption key generation
def generate_fernet_key():
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(str(time.time() + os.getpid()).encode()))
    return Fernet(key)

cipher = generate_fernet_key()

# 1. Comprehensive debugger detection
class DebuggerDetector:
    @staticmethod
    def check_windows():
        if os.name != "nt":
            return False
        kernel32 = ctypes.windll.kernel32
        is_debugger_present = kernel32.IsDebuggerPresent()
        remote_debugger = ctypes.c_int(0)
        kernel32.CheckRemoteDebuggerPresent(kernel32.GetCurrentProcess(), ctypes.byref(remote_debugger))
        return is_debugger_present or remote_debugger.value

    @staticmethod
    def check_linux():
        if os.name == "nt":
            return False
        try:
            with open("/proc/self/stat", "r") as f:
                return int(f.read().split()[6]) != os.getpid()
        except:
            return False

    @staticmethod
    def check_timing():
        t = time.perf_counter()
        [x for x in range(10000)]
        return (time.perf_counter() - t) > 0.5

    @staticmethod
    def check_memory():
        try:
            ctypes.c_void_p(0).value
            return False
        except:
            return True

    def is_active(self):
        return any([self.check_windows(), self.check_linux(), self.check_timing(), self.check_memory()])

# 2. Lock down tracing and signals
def lockdown_system():
    sys.settrace = lambda *args: None
    sys.setprofile = lambda *args: None
    if os.name == "nt":
        signal.signal(signal.SIGBREAK, lambda *args: os._exit(1))
        signal.signal(signal.SIGINT, lambda *args: os._exit(1))
        signal.signal(signal.SIGTERM, lambda *args: os._exit(1))
    else:
        signal.signal(signal.SIGINT, lambda *args: os._exit(1))
        with suppress(AttributeError):
            signal.signal(signal.SIGTRAP, lambda *args: os._exit(1))
            signal.signal(signal.SIGSEGV, lambda *args: os._exit(1))
    sys.setswitchinterval(0.00001)

# 3. Protect imports and built-ins
class SystemGuard:
    RESTRICTED = {"pdb", "pydevd", "tracemalloc", "debugpy", "inspect", "trace", "dis", "opcode", "sys", "os"}

    def __init__(self):
        self.original_import = __import__
        self.original_exec = builtins.exec
        self.original_eval = builtins.eval
        self.original_getattr = getattr

    def restrict_import(self, name, *args, **kwargs):
        if name in self.RESTRICTED:
            os._exit(2)
        return self.original_import(name, *args, **kwargs)

    def restrict_exec(self, code, *args, **kwargs):
        if isinstance(code, str) and any(kw in code.lower() for kw in self.RESTRICTED):
            os._exit(3)
        return self.original_exec(code, *args, **kwargs)

    def restrict_eval(self, code, *args, **kwargs):
        if isinstance(code, str) and any(kw in code.lower() for kw in self.RESTRICTED):
            os._exit(4)
        return self.original_eval(code, *args, **kwargs)

    def restrict_getattr(self, obj, name, *args, **kwargs):
        if name in {"__code__", "co_code", "func_code"}:
            raise AttributeError("Access Denied")
        return self.original_getattr(obj, name, *args, **kwargs)

    def apply(self):
        builtins.__import__ = self.restrict_import
        builtins.exec = self.restrict_exec
        builtins.eval = self.restrict_eval
        builtins.getattr = self.restrict_getattr
        for mod in self.RESTRICTED:
            sys.modules[mod] = None

# 4. Ultimate sandbox/VM detection
class SandboxDetector:
    VM_SIGNALS = [("/sys/hypervisor", "Hyper-V"), ("/proc/scsi/scsi", "VMware"), ("/dev/vboxguest", "VirtualBox")]

    def check_hardware(self):
        try:
            return os.cpu_count() <= 2
        except:
            return False

    def check_files(self):
        return any(os.path.exists(f) for f, _ in self.VM_SIGNALS)

    def check_registry(self):
        if os.name == "nt":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\VMware, Inc.")
                winreg.CloseKey(key)
                return True
            except:
                return False
        return False

    def check_processes(self):
        vm_procs = ["vboxservice.exe", "vmtoolsd.exe", "qemu-ga.exe"]
        if os.name == "nt":
            try:
                output = subprocess.check_output("tasklist", shell=True, text=True).lower()
                return any(p in output for p in vm_procs)
            except:
                return False
        return False

    def is_sandbox(self):
        return any([self.check_hardware(), self.check_files(), self.check_registry(), self.check_processes()])

# 5. Highly sensitive monitoring thread
class AntiDebugThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.detector = DebuggerDetector()

    def run(self):
        while True:
            try:
                if self.detector.is_active():
                    self.defense_mechanism()
                time.sleep(random.uniform(0.01, 0.1))
            except Exception as e:
                print(f"AntiDebugThread Error: {e}")
                os._exit(5)

    def defense_mechanism(self):
        with suppress(Exception):
            ctypes.string_at(0)
        os.write(1, b"Intrusion Detected!\n")
        os._exit(5)

# 6. Advanced bytecode encryption
class CodeProtector:
    def __init__(self):
        self.cipher = cipher

    def encrypt_bytecode(self, code_obj):
        raw = marshal.dumps(code_obj)
        compressed = zlib.compress(raw, level=9)
        encrypted = self.cipher.encrypt(compressed)
        return base64.b64encode(encrypted).decode()

    def decrypt_bytecode(self, encrypted):
        decoded = base64.b64decode(encrypted)
        decrypted = self.cipher.decrypt(decoded)
        raw = zlib.decompress(decrypted)
        return marshal.loads(raw)

    def protect(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Encrypt and decrypt the function's bytecode
                encrypted_code = self.encrypt_bytecode(func.__code__)
                decrypted_code = self.decrypt_bytecode(encrypted_code)
                new_func = types.FunctionType(decrypted_code, globals(), func.__name__)
                return new_func(*args, **kwargs)
            except Exception as e:
                print(f"Protection Error: {e}")
                os._exit(1)
        return wrapper

# 7. Comprehensive obfuscation
class Obfuscator:
    @staticmethod
    def junk_globals():
        for _ in range(1000):
            globals()[f"obf_{random.randint(0, 99999999)}"] = random.choice([
                None,
                random.randint(0, 9999999),
                lambda x: x,
                b"\x00" * random.randint(10, 100)
            ])

    @staticmethod
    def junk_functions():
        for _ in range(500):
            name = f"fake_{random.randint(0, 9999999)}"
            globals()[name] = lambda *args: random.randint(0, 999)

    @staticmethod
    def spoof_bytecode(func):
        new_code = types.CodeType(
            0, 0, 0, 0, 0, 0, b"\x00" * 2048, (), (), (), "<obfuscated>", "<fake>",
            0, b"", (), (), (), ()
        )
        func.__code__ = new_code
        return func

# 8. High-level string protection
class StringProtector:
    def __init__(self):
        self.cipher = cipher

    def encrypt(self, s):
        return self.cipher.encrypt(s.encode())

    def decrypt(self, enc):
        return self.cipher.decrypt(enc).decode()

# 9. Process spoofing and self-destruction
class ProcessSpoofer:
    @staticmethod
    def spoof():
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(f"ntoskrnl_{random.randint(100000, 999999)}")
        else:
            os.write(1, b"\x1b]0;systemd\x07")

    @staticmethod
    def self_destruct():
        try:
            with open(__file__, "wb") as f:
                f.write(os.urandom(4096))
            for f in os.listdir():
                if f.endswith(".pyc"):
                    os.remove(f)
        except:
            pass
        finally:
            os._exit(6)

# 10. Anti-memory dump
def anti_memory_dump():
    if os.name == "nt":
        try:
            ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
            ctypes.windll.kernel32.RtlZeroMemory(ctypes.c_void_p(random.randint(0, 0x1000)), 1024)
        except:
            pass
    else:
        os.write(1, b"\x00" * 1024)

# 11. Protect the module itself
cp = CodeProtector()

@cp.protect
def initialize_protection():
    guard = SystemGuard()
    sandbox = SandboxDetector()
    obf = Obfuscator()
    spoofer = ProcessSpoofer()

    lockdown_system()
    guard.apply()
    obf.junk_globals()
    obf.junk_functions()
    spoofer.spoof()
    anti_memory_dump()

    thread = AntiDebugThread()
    thread.start()

    if sandbox.is_sandbox() or DebuggerDetector().is_active():
        spoofer.self_destruct()

    atexit.register(spoofer.self_destruct)
    print("Anti-Protection Initialized!")

# 12. Export protection for QUANLY.py
def protect_main():
    initialize_protection()
    return cp.protect

if __name__ == "__main__":
    protect_main()
