from struct import pack, unpack

from network.packet.PacketWriter import *
from database.realm.RealmDatabaseManager import *


class CharEnumHandler(object):

    @staticmethod
    def handle(world_session, socket, packet):
        characters = RealmDatabaseManager.account_get_characters(world_session.account_mgr.account.id)
        count = len(characters)

        data = pack('<B', count)
        for character in characters:
            data += CharEnumHandler.get_char_packet(character)
        socket.sendall(PacketWriter.get_packet(OpCode.SMSG_CHAR_ENUM, data))

        return 0

    @staticmethod
    def get_char_packet(character):
        name_bytes = PacketWriter.string_to_bytes(character.name)
        char_fmt = '<Q%usBBBBBBBBBIIfffIIIIIBIBIBIBIBIBIBIBIBIBIBIBIBIBIBIBIBIBIBIB' % len(name_bytes)
        char_packet = pack(
            char_fmt,
            character.guid,
            name_bytes,
            character.race,
            character.class_,
            character.gender,
            character.skin,
            character.face,
            character.hairstyle,
            character.haircolour,
            character.facialhair,
            character.level,
            character.zone,
            character.map,
            character.position_x,
            character.position_y,
            character.position_z,
            0,  # TODO: Handle Guild GUID,
            0,  # TODO: Handle PetDisplayInfo
            0,  # TODO: Handle PetLevel
            0,  # TODO: Handle PetFamily
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # TODO: Handle ItemInventory
        )
        return char_packet
