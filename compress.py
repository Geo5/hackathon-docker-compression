import sys
from pathlib import Path
import subprocess

COMMANDS = [
    "FROM",
    "RUN",
    "CMD",
    "LABEL",
    "MAINTAINER",
    "EXPOSE",
    "ENV",
    "ADD",
    "COPY",
    "ENTRYPOINT",
    "VOLUME",
    "USER",
    "WORKDIR",
    "ARG",
    "ONBUILD",
    "STOPSIGNAL",
    "HEALTHCHECK",
    "SHELL",
]

FST_LETTER: dict[str, list[str]] = {}
for c in COMMANDS:
    if c[0] not in FST_LETTER:
        FST_LETTER[c[0]] = []
    FST_LETTER[c[0]].append(c)


def compress(infile):
    outfile = Path(str(infile) + ".compressed")
    newlines = []
    append_to_last = False
    append_next = False
    for line in infile.open("r"):
        append_to_last = append_next
        line = line.strip()
        # empty
        if not line:
            continue
        # comment but not parser directive
        if line.startswith("#") and "syntax=" not in line and "escape=" not in line:
            continue
        words = line.split(" ")
        # Lowercase command
        if words and words[0] in COMMANDS:
            if len(FST_LETTER[words[0][0]]) == 1:
                words[0] = words[0][0]
            elif words[0][0] != "E":
                words[0] = words[0][:2]
            else:
                words[0] = words[0][:3]
            words[0] = words[0].lower()
            line = " ".join(words)
        if line[-1] == "\\":
            line = line[:-1]
            append_next = True
        else:
            append_next = False
        if append_to_last:
            newlines[-1] += line
        else:
            newlines.append(line)
    newcontent = "\n".join(newlines)
    tempfile = Path(str(outfile) + "_temp")
    tempfile.write_text(newcontent)
    subprocess.call(
        [
            "zstd",
            "--ultra",
            "-22",
            "-f",
            "-o",
            str(outfile),
            str(tempfile),
        ]
    )
    tempfile.unlink()


def decompress(infile):
    outfile = infile.with_suffix(".decompressed")
    tempfile = Path(str(outfile) + "_temp")
    subprocess.call(
        [
            "zstd",
            "-d",
            "-f",
            "-o",
            str(tempfile),
            str(infile),
        ]
    )
    newlines = []
    for line in tempfile.open("r"):
        line = line.strip()
        # empty
        if not line:
            continue
        words = line.split(" ")
        # Lowercase command
        if words and words[0][0].upper() in FST_LETTER:
            choices = FST_LETTER[words[0][0].upper()]
            try:
                if len(choices) == 1:
                    words[0] = choices[0]
                elif len(choices) == 2:
                    words[0] = next(
                        choice
                        for choice in choices
                        if choice.startswith(words[0][:2].upper())
                    )
                else:
                    words[0] = next(
                        choice
                        for choice in choices
                        if choice.startswith(words[0][:3].upper())
                    )
            except StopIteration:
                pass
            words[0] = words[0].upper()
            line = " ".join(words)
        newlines.append(line)
    newcontent = "\n".join(newlines)
    outfile.write_text(newcontent)
    tempfile.unlink()


def main(args):
    infile = Path(args[0])
    if infile.suffix == ".compressed":
        decompress(infile)
    else:
        compress(infile)


if __name__ == "__main__":
    main(sys.argv[1:])