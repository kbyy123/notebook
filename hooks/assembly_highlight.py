"""Register a cleaner x86-64 lexer for `assembly` Markdown code fences."""

from __future__ import annotations

import re

from pygments.lexer import Lexer
from pygments.lexers import _lexer_cache, _mapping
from pygments.lexers.asm import GasLexer
from pygments.token import Generic, Name, Number, Operator, Punctuation, Text


class X8664AssemblyLexer(Lexer):
    """Highlight x86-64 assembly without mangling hex2raw byte payloads.

    CS:APP notes often mix real assembly, objdump output, and raw byte payloads
    in the same fenced block. Pygments' GAS lexer handles the first case, but it
    treats byte-only lines such as `48 83 ec 10` as assembly identifiers. This
    lexer keeps those bytes visually uniform and delegates ordinary assembly
    lines to the built-in GAS lexer.
    """

    name = "X86-64 Assembly"
    aliases = ["assembly", "x86-64", "x86_64"]
    filenames = []
    mimetypes = ["text/x-x86-64-assembly"]

    _byte_line = re.compile(r"^(\s*)((?:[0-9A-Fa-f]{2}(?:\s+|$))+)$")
    _objdump_line = re.compile(
        r"^(\s*)([0-9A-Fa-f]+)(:)(\s*)((?:[0-9A-Fa-f]{2}\s+)*)(.*?)(\s*)$"
    )
    _gdb_dump_line = re.compile(
        r"^(\s*(?:=>\s*)?)(0x[0-9A-Fa-f]+)(\s+)(<\+[0-9]+>)(:)(\s*)(.*?)(\s*)$"
    )
    _gadget_line = re.compile(r"^(\s*)(0x[0-9A-Fa-f]+)(\s+)(.*?)(\s*)$")
    _label_line = re.compile(r"^(\s*)([0-9A-Fa-f]+)(\s+)(<[^>]+>)(:)(\s*)$")
    _shell_prompt = re.compile(r"^(.+[@:].*\$\s+)(.*?)(\s*)$")
    _objdump_heading = re.compile(r"^\s*Disassembly of section .+:\s*$")
    _gdb_dump_heading = re.compile(r"^\s*Dump of assembler code for function .+:\s*$")
    _gdb_prompt = re.compile(r"^\s*\(gdb\)\s+.*$")
    _terminal_output = re.compile(
        r"^\s*(Cookie:|Type string:|Valid solution|PASS:|NICE JOB|Misfire:|"
        r"Touch[0-9]!:|FAILED:|FAIL:|End of assembler dump\.|\$[0-9]+\s*=)"
    )
    _bare_hex_address = re.compile(r"^[0-9A-Fa-f]{3,}$")
    _address_ref = re.compile(r"(0x[0-9A-Fa-f]{4,})(\s+<[^>]+>)?")

    def __init__(self, **options):
        super().__init__(**options)
        self._gas = GasLexer(**options)

    def get_tokens_unprocessed(self, text):
        offset = 0
        for line in text.splitlines(keepends=True):
            body = line[:-1] if line.endswith("\n") else line
            newline = "\n" if line.endswith("\n") else ""

            for token_offset, token, value in self._get_line_tokens(body):
                yield offset + token_offset, token, value

            if newline:
                yield offset + len(body), Text.Whitespace, newline
            offset += len(line)

    def _get_line_tokens(self, line):
        if not line:
            return

        if self._objdump_heading.match(line):
            yield 0, Generic.Heading, line
            return

        if self._gdb_dump_heading.match(line):
            yield 0, Generic.Heading, line
            return

        if self._gdb_prompt.match(line):
            yield 0, Generic.Prompt, line
            return

        if self._terminal_output.match(line):
            yield 0, Text, line
            return

        byte_match = self._byte_line.match(line)
        if byte_match:
            yield from self._highlight_byte_line(byte_match)
            return

        gdb_dump_match = self._gdb_dump_line.match(line)
        if gdb_dump_match:
            yield from self._highlight_gdb_dump_line(gdb_dump_match)
            return

        gadget_match = self._gadget_line.match(line)
        if gadget_match:
            yield from self._highlight_gadget_line(gadget_match)
            return

        label_match = self._label_line.match(line)
        if label_match:
            yield from self._highlight_label_line(label_match)
            return

        objdump_match = self._objdump_line.match(line)
        if objdump_match and (
            objdump_match.group(5).strip() or objdump_match.group(6).strip()
        ):
            yield from self._highlight_objdump_line(objdump_match)
            return

        prompt_match = self._shell_prompt.match(line)
        if prompt_match:
            yield from self._highlight_shell_prompt(prompt_match)
            return

        yield from self._offset_tokens(0, self._gas.get_tokens_unprocessed(line))

    def _highlight_byte_line(self, match):
        leading, bytes_text = match.groups()
        if leading:
            yield 0, Text.Whitespace, leading
        yield from self._highlight_bytes(len(leading), bytes_text)

    def _highlight_label_line(self, match):
        leading, address, space, label, colon, trailing = match.groups()
        pos = 0
        yield pos, Text.Whitespace, leading
        pos += len(leading)
        yield pos, Generic.Output, address
        pos += len(address)
        yield pos, Text.Whitespace, space
        pos += len(space)
        yield pos, Name.Label, label
        pos += len(label)
        yield pos, Punctuation, colon
        pos += len(colon)
        if trailing:
            yield pos, Text.Whitespace, trailing

    def _highlight_gadget_line(self, match):
        leading, address, space, expression, trailing = match.groups()
        pos = 0
        if leading:
            yield pos, Text.Whitespace, leading
            pos += len(leading)
        yield pos, Generic.Output, address
        pos += len(address)
        yield pos, Text.Whitespace, space
        pos += len(space)
        yield from self._highlight_gadget_expression(pos, expression)
        pos += len(expression)
        if trailing:
            yield pos, Text.Whitespace, trailing

    def _highlight_gdb_dump_line(self, match):
        marker, address, space, offset, colon, after_colon, instruction, trailing = (
            match.groups()
        )
        pos = 0
        yield pos, Text.Whitespace, marker
        pos += len(marker)
        yield pos, Generic.Output, address
        pos += len(address)
        yield pos, Text.Whitespace, space
        pos += len(space)
        yield pos, Generic.Output, offset
        pos += len(offset)
        yield pos, Punctuation, colon
        pos += len(colon)
        yield pos, Text.Whitespace, after_colon
        pos += len(after_colon)
        yield from self._highlight_instruction(pos, instruction)
        pos += len(instruction)
        if trailing:
            yield pos, Text.Whitespace, trailing

    def _highlight_objdump_line(self, match):
        leading, address, colon, after_colon, bytes_text, instruction, trailing = (
            match.groups()
        )
        if re.fullmatch(r"\s*[0-9A-Fa-f]{2}\s*", instruction):
            bytes_text += instruction
            instruction = ""

        pos = 0
        yield pos, Text.Whitespace, leading
        pos += len(leading)
        yield pos, Generic.Output, address
        pos += len(address)
        yield pos, Punctuation, colon
        pos += len(colon)
        yield pos, Text.Whitespace, after_colon
        pos += len(after_colon)
        yield from self._highlight_bytes(pos, bytes_text)
        pos += len(bytes_text)
        yield from self._highlight_instruction(pos, instruction)
        pos += len(instruction)
        if trailing:
            yield pos, Text.Whitespace, trailing

    def _highlight_shell_prompt(self, match):
        prompt, command, trailing = match.groups()
        pos = 0
        yield pos, Generic.Prompt, prompt
        pos += len(prompt)
        yield from self._highlight_command(pos, command)
        pos += len(command)
        if trailing:
            yield pos, Text.Whitespace, trailing

    def _highlight_command(self, start, command):
        for match in re.finditer(r"\S+|\s+", command):
            value = match.group(0)
            pos = start + match.start()
            if value.isspace():
                yield pos, Text.Whitespace, value
            elif value in {"<", ">", "|"}:
                yield pos, Operator, value
            elif value in {"cat", "./hex2raw", "./ctarget", "./rtarget"}:
                yield pos, Name.Builtin, value
            else:
                yield pos, Text, value

    def _highlight_gadget_expression(self, start, expression):
        for match in re.finditer(r"%[A-Za-z0-9]+|-->|[+]|[A-Za-z_][A-Za-z0-9_]*|\s+|.", expression):
            value = match.group(0)
            pos = start + match.start()
            if value.isspace():
                yield pos, Text.Whitespace, value
            elif value.startswith("%"):
                yield pos, Name.Variable, value
            elif value == "-->" or value == "+":
                yield pos, Operator, value
            elif value in {"popq", "pushq", "movq", "retq", "touch3"}:
                yield pos, Name.Function, value
            else:
                yield pos, Text, value

    def _highlight_instruction(self, start, instruction):
        cursor = 0
        for match in self._address_ref.finditer(instruction):
            if match.start() > cursor:
                segment = instruction[cursor : match.start()]
                yield from self._offset_tokens(
                    start + cursor, self._gas.get_tokens_unprocessed(segment)
                )

            address, label = match.groups()
            yield start + match.start(1), Generic.Output, address
            if label:
                label_start = match.start(2)
                space_length = len(label) - len(label.lstrip())
                if space_length:
                    yield start + label_start, Text.Whitespace, label[:space_length]
                yield start + label_start + space_length, Name.Label, label[space_length:]
            cursor = match.end()

        if cursor < len(instruction):
            yield from self._offset_tokens(
                start + cursor, self._gas.get_tokens_unprocessed(instruction[cursor:])
            )

    def _highlight_bytes(self, start, text):
        for match in re.finditer(r"[0-9A-Fa-f]{2}|\s+", text):
            value = match.group(0)
            token = Text if not value.isspace() else Text.Whitespace
            yield start + match.start(), token, value

    def _offset_tokens(self, start, tokens):
        for pos, token, value in tokens:
            if token is Number.Hex and self._bare_hex_address.match(value):
                token = Generic.Output
            yield start + pos, token, value


def register_assembly_lexer() -> None:
    _lexer_cache[X8664AssemblyLexer.name] = X8664AssemblyLexer
    _mapping.LEXERS["X8664AssemblyLexer"] = (
        __name__,
        X8664AssemblyLexer.name,
        tuple(X8664AssemblyLexer.aliases),
        tuple(X8664AssemblyLexer.filenames),
        tuple(X8664AssemblyLexer.mimetypes),
    )


register_assembly_lexer()


def on_startup(command, dirty):
    register_assembly_lexer()
