import platform
import sys

print("== HE OS MATRIX CHECK ==")
print("system:", platform.system())
print("release:", platform.release())
print("machine:", platform.machine())
print("python:", sys.version.split()[0])
assert platform.system() in ("Linux", "Darwin", "Windows"), "unexpected OS"
print("RESULT: PASS")
sys.exit(0)
