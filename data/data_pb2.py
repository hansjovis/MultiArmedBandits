# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='data.proto',
  package='',
  serialized_pb='\n\ndata.proto\"\xd9\x04\n\x03Run\x12\x0b\n\x03\x61ge\x18\x01 \x02(\x05\x12\x11\n\tproductid\x18\x02 \x02(\x05\x12\r\n\x05runid\x18\x03 \x02(\x05\x12\t\n\x01i\x18\x04 \x02(\x05\x12\n\n\x02ID\x18\x05 \x02(\x05\x12\x11\n\tsuccesses\x18\x06 \x02(\x05\x12\x10\n\x08\x66\x61ilures\x18\x07 \x02(\x05\x12\r\n\x05price\x18\x08 \x02(\x02\x12\x19\n\x05\x61gent\x18\t \x02(\x0e\x32\n.Run.Agent\x12\x1f\n\x08language\x18\n \x02(\x0e\x32\r.Run.Language\x12\x1d\n\x07referer\x18\x0b \x02(\x0e\x32\x0c.Run.Referer\x12\x1b\n\x06header\x18\x0c \x02(\x0e\x32\x0b.Run.Header\x12\x1b\n\x06\x61\x64type\x18\r \x02(\x0e\x32\x0b.Run.Adtype\x12\x19\n\x05\x63olor\x18\x0e \x02(\x0e\x32\n.Run.Color\"4\n\x05\x41gent\x12\x07\n\x03OSX\x10\x00\x12\x0b\n\x07Windows\x10\x01\x12\t\n\x05Linux\x10\x02\x12\n\n\x06Mobile\x10\x03\"*\n\x08Language\x12\x06\n\x02\x45N\x10\x00\x12\x06\n\x02NL\x10\x01\x12\x06\n\x02GE\x10\x02\x12\x06\n\x02NA\x10\x03\"\'\n\x07Referer\x12\n\n\x06Google\x10\x00\x12\x08\n\x04\x42ing\x10\x01\x12\x06\n\x02NO\x10\x02\".\n\x06Header\x12\x08\n\x04\x46IVE\x10\x00\x12\x0b\n\x07\x46IFTEEN\x10\x01\x12\r\n\tTHIRTFIVE\x10\x02\"0\n\x06\x41\x64type\x12\x0e\n\nskyscraper\x10\x00\x12\n\n\x06square\x10\x01\x12\n\n\x06\x62\x61nner\x10\x02\";\n\x05\x43olor\x12\t\n\x05green\x10\x00\x12\x08\n\x04\x62lue\x10\x01\x12\x07\n\x03red\x10\x02\x12\t\n\x05\x62lack\x10\x03\x12\t\n\x05white\x10\x04\"\x1d\n\x08\x44\x61taBase\x12\x11\n\x03run\x18\x01 \x03(\x0b\x32\x04.Run')



_RUN_AGENT = _descriptor.EnumDescriptor(
  name='Agent',
  full_name='Run.Agent',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OSX', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Windows', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Linux', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Mobile', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=320,
  serialized_end=372,
)

_RUN_LANGUAGE = _descriptor.EnumDescriptor(
  name='Language',
  full_name='Run.Language',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='EN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NL', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NA', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=374,
  serialized_end=416,
)

_RUN_REFERER = _descriptor.EnumDescriptor(
  name='Referer',
  full_name='Run.Referer',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Google', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Bing', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NO', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=418,
  serialized_end=457,
)

_RUN_HEADER = _descriptor.EnumDescriptor(
  name='Header',
  full_name='Run.Header',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FIVE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIFTEEN', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='THIRTFIVE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=459,
  serialized_end=505,
)

_RUN_ADTYPE = _descriptor.EnumDescriptor(
  name='Adtype',
  full_name='Run.Adtype',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='skyscraper', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='square', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='banner', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=507,
  serialized_end=555,
)

_RUN_COLOR = _descriptor.EnumDescriptor(
  name='Color',
  full_name='Run.Color',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='green', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='blue', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='red', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='black', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='white', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=557,
  serialized_end=616,
)


_RUN = _descriptor.Descriptor(
  name='Run',
  full_name='Run',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='age', full_name='Run.age', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='productid', full_name='Run.productid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='runid', full_name='Run.runid', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='i', full_name='Run.i', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ID', full_name='Run.ID', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='successes', full_name='Run.successes', index=5,
      number=6, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='failures', full_name='Run.failures', index=6,
      number=7, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='price', full_name='Run.price', index=7,
      number=8, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='agent', full_name='Run.agent', index=8,
      number=9, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='language', full_name='Run.language', index=9,
      number=10, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='referer', full_name='Run.referer', index=10,
      number=11, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='header', full_name='Run.header', index=11,
      number=12, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='adtype', full_name='Run.adtype', index=12,
      number=13, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='color', full_name='Run.color', index=13,
      number=14, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RUN_AGENT,
    _RUN_LANGUAGE,
    _RUN_REFERER,
    _RUN_HEADER,
    _RUN_ADTYPE,
    _RUN_COLOR,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=15,
  serialized_end=616,
)


_DATABASE = _descriptor.Descriptor(
  name='DataBase',
  full_name='DataBase',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='run', full_name='DataBase.run', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=618,
  serialized_end=647,
)

_RUN.fields_by_name['agent'].enum_type = _RUN_AGENT
_RUN.fields_by_name['language'].enum_type = _RUN_LANGUAGE
_RUN.fields_by_name['referer'].enum_type = _RUN_REFERER
_RUN.fields_by_name['header'].enum_type = _RUN_HEADER
_RUN.fields_by_name['adtype'].enum_type = _RUN_ADTYPE
_RUN.fields_by_name['color'].enum_type = _RUN_COLOR
_RUN_AGENT.containing_type = _RUN;
_RUN_LANGUAGE.containing_type = _RUN;
_RUN_REFERER.containing_type = _RUN;
_RUN_HEADER.containing_type = _RUN;
_RUN_ADTYPE.containing_type = _RUN;
_RUN_COLOR.containing_type = _RUN;
_DATABASE.fields_by_name['run'].message_type = _RUN
DESCRIPTOR.message_types_by_name['Run'] = _RUN
DESCRIPTOR.message_types_by_name['DataBase'] = _DATABASE

class Run(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RUN

  # @@protoc_insertion_point(class_scope:Run)

class DataBase(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DATABASE

  # @@protoc_insertion_point(class_scope:DataBase)


# @@protoc_insertion_point(module_scope)