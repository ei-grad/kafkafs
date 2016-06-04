# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fuse.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='fuse.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\nfuse.proto\"\xee\x05\n\nFuseChange\x12\x0c\n\x04uuid\x18\x01 \x01(\x0c\x12!\n\x02op\x18\x02 \x01(\x0e\x32\x15.FuseChange.Operation\x12\x0c\n\x04path\x18\x03 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\x0c\x12\x0e\n\x06offset\x18\x05 \x01(\x04\x12\x0c\n\x04mode\x18\x06 \x01(\r\x12\x1f\n\x05\x66lags\x18\x07 \x03(\x0e\x32\x10.FuseChange.Flag\x12\x0b\n\x03uid\x18\x08 \x01(\r\x12\x0b\n\x03gid\x18\t \x01(\r\x12\x0f\n\x07\x66h_uuid\x18\n \x01(\x0c\x12\x10\n\x08\x64\x61tasync\x18\x0b \x01(\x08\x12\x0b\n\x03src\x18\x0c \x01(\t\x12\x0e\n\x06length\x18\r \x01(\r\x12\r\n\x05\x61time\x18\x0e \x01(\x02\x12\r\n\x05mtime\x18\x0f \x01(\x02\"\xac\x01\n\tOperation\x12\t\n\x05\x43HMOD\x10\x00\x12\t\n\x05\x43HOWN\x10\x01\x12\n\n\x06\x43REATE\x10\x03\x12\t\n\x05\x46SYNC\x10\x04\x12\x08\n\x04LINK\x10\x05\x12\t\n\x05MKDIR\x10\x06\x12\x08\n\x04OPEN\x10\x07\x12\x0b\n\x07RELEASE\x10\x08\x12\t\n\x05RMDIR\x10\t\x12\x0b\n\x07SYMLINK\x10\n\x12\x0c\n\x08TRUNCATE\x10\x0b\x12\n\n\x06UNLINK\x10\x0c\x12\t\n\x05UTIME\x10\r\x12\t\n\x05WRITE\x10\x0e\"\xac\x02\n\x04\x46lag\x12\x0c\n\x08O_RDONLY\x10\x00\x12\x0c\n\x08O_WRONLY\x10\x01\x12\n\n\x06O_RDWR\x10\x02\x12\x0c\n\x08O_APPEND\x10\x03\x12\x0b\n\x07O_ASYNC\x10\x04\x12\r\n\tO_CLOEXEC\x10\x05\x12\x0b\n\x07O_CREAT\x10\x06\x12\x0c\n\x08O_DIRECT\x10\x07\x12\x0f\n\x0bO_DIRECTORY\x10\x08\x12\x0b\n\x07O_DSYNC\x10\t\x12\n\n\x06O_EXCL\x10\n\x12\x0f\n\x0bO_LARGEFILE\x10\x0b\x12\r\n\tO_NOATIME\x10\x0c\x12\x0c\n\x08O_NOCTTY\x10\r\x12\x0e\n\nO_NOFOLLOW\x10\x0e\x12\x0e\n\nO_NONBLOCK\x10\x0f\x12\n\n\x06O_PATH\x10\x10\x12\x0b\n\x07O_RSYNC\x10\x11\x12\n\n\x06O_SYNC\x10\x12\x12\r\n\tO_TMPFILE\x10\x13\x12\x0b\n\x07O_TRUNC\x10\x14\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_FUSECHANGE_OPERATION = _descriptor.EnumDescriptor(
  name='Operation',
  full_name='FuseChange.Operation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CHMOD', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHOWN', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATE', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FSYNC', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LINK', index=4, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MKDIR', index=5, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPEN', index=6, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RELEASE', index=7, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RMDIR', index=8, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SYMLINK', index=9, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRUNCATE', index=10, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNLINK', index=11, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UTIME', index=12, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WRITE', index=13, number=14,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=290,
  serialized_end=462,
)
_sym_db.RegisterEnumDescriptor(_FUSECHANGE_OPERATION)

_FUSECHANGE_FLAG = _descriptor.EnumDescriptor(
  name='Flag',
  full_name='FuseChange.Flag',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='O_RDONLY', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_WRONLY', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_RDWR', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_APPEND', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_ASYNC', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_CLOEXEC', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_CREAT', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_DIRECT', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_DIRECTORY', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_DSYNC', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_EXCL', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_LARGEFILE', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_NOATIME', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_NOCTTY', index=13, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_NOFOLLOW', index=14, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_NONBLOCK', index=15, number=15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_PATH', index=16, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_RSYNC', index=17, number=17,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_SYNC', index=18, number=18,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_TMPFILE', index=19, number=19,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='O_TRUNC', index=20, number=20,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=465,
  serialized_end=765,
)
_sym_db.RegisterEnumDescriptor(_FUSECHANGE_FLAG)


_FUSECHANGE = _descriptor.Descriptor(
  name='FuseChange',
  full_name='FuseChange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uuid', full_name='FuseChange.uuid', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='op', full_name='FuseChange.op', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='path', full_name='FuseChange.path', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='FuseChange.data', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='offset', full_name='FuseChange.offset', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mode', full_name='FuseChange.mode', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='flags', full_name='FuseChange.flags', index=6,
      number=7, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uid', full_name='FuseChange.uid', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gid', full_name='FuseChange.gid', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fh_uuid', full_name='FuseChange.fh_uuid', index=9,
      number=10, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='datasync', full_name='FuseChange.datasync', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='src', full_name='FuseChange.src', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='length', full_name='FuseChange.length', index=12,
      number=13, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='atime', full_name='FuseChange.atime', index=13,
      number=14, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mtime', full_name='FuseChange.mtime', index=14,
      number=15, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FUSECHANGE_OPERATION,
    _FUSECHANGE_FLAG,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=765,
)

_FUSECHANGE.fields_by_name['op'].enum_type = _FUSECHANGE_OPERATION
_FUSECHANGE.fields_by_name['flags'].enum_type = _FUSECHANGE_FLAG
_FUSECHANGE_OPERATION.containing_type = _FUSECHANGE
_FUSECHANGE_FLAG.containing_type = _FUSECHANGE
DESCRIPTOR.message_types_by_name['FuseChange'] = _FUSECHANGE

FuseChange = _reflection.GeneratedProtocolMessageType('FuseChange', (_message.Message,), dict(
  DESCRIPTOR = _FUSECHANGE,
  __module__ = 'fuse_pb2'
  # @@protoc_insertion_point(class_scope:FuseChange)
  ))
_sym_db.RegisterMessage(FuseChange)


# @@protoc_insertion_point(module_scope)
