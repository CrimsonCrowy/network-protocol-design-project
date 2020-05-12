import libnacl.sealed
import libnacl.public

keypair = libnacl.public.SecretKey()

print()
print('Public Key:', keypair.hex_pk().decode("ascii"))
print('Secret Key:', keypair.hex_sk().decode("ascii"))
print()