import re
import pdfplumber
import json

def parse_spell_block(block):
    lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
    if len(lines) < 6:
        return None  # Not enough lines for a spell

    spell = {}

    # 1. Spell Name
    spell['spell_name'] = lines[0]

    # 2. Level/School/Classes (always 2nd line for PHB)
    lvl_line = lines[1]
    # Pattern 1: '2nd-level abjuration (cleric, paladin)'
    m = re.match(r"(?i)^([1-9][a-z]{2})-level ([A-Za-z]+) \(([^)]+)\)$", lvl_line)
    if m:
        spell['spell_level'] = int(m.group(1)[0])  # '2nd' -> 2
        spell['spell_type'] = m.group(2)
        spell['spell_user_classes'] = [c.strip().capitalize() for c in m.group(3).split(',')]
    else:
        # Pattern 2: 'Conjuration cantrip (sorcerer, wizard)'
        m = re.match(r"(?i)^([A-Za-z]+) cantrip \(([^)]+)\)$", lvl_line)
        if m:
            spell['spell_level'] = "cantrip"
            spell['spell_type'] = m.group(1)
            spell['spell_user_classes'] = [c.strip().capitalize() for c in m.group(2).split(',')]
        else:
            return None  # Something is wrong

    # 3–6. Key-Value Lines
    kmap = {
        'casting time': 'casting_time',
        'range': 'range',
        'components': 'components',
        'duration': 'duration'
    }
    idx = 2
    for i in range(4):
        key, val = lines[idx+i].split(':', 1)
        spell[kmap[key.lower().strip()]] = val.strip()
    idx += 4

    # 7. Description: rest, joined, with newlines
    desc_lines = lines[idx:]
    desc = '\n'.join(desc_lines).strip()
    spell['description'] = desc

    return spell

def is_spell_name(line):
    return (
        len(line.split()) <= 4
        and re.match(r"^[A-Z][A-Za-z\s’'-]+$", line)
        and ':' not in line
        and not any(str(d) for d in range(10))
    )

def split_spell_blocks(text):
    lines = text.splitlines()
    blocks = []
    current = []
    for line in lines:
        if is_spell_name(line):
            if current:
                blocks.append('\n'.join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append('\n'.join(current))
    return blocks

def extract_columns(page):
    W = page.width
    midpoint = W * 0.5
    left, right = [], []
    for word in page.extract_words():
        if word['x0'] < midpoint:
            left.append(word)
        else:
            right.append(word)
    def group_words(words):
        lines = {}
        for w in words:
            y = round(w['top'], 1)
            lines.setdefault(y, []).append(w['text'])
        out = [' '.join(lines[y]) for y in sorted(lines)]
        return out
    return group_words(left), group_words(right)

def main(pdf_path, out_json):
    all_text = []
    counter = 0
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            left, right = extract_columns(page)
            # Combine in reading order: left, right
            all_text.extend(left)
            all_text.extend(right)
            counter += 1

            if counter % 10 == 0:
                print(f"Processed {counter} pages...")
    # Now combine all lines into a big text
    text = '\n'.join(all_text)
    
    # Save the text to a file
    with open("spells_phb.txt", 'w', encoding='utf-8') as f:
        f.write(text)

    ## Get blocks
    #blocks = split_spell_blocks(text)
    ## Parse blocks
    #spells = []
    #for block in blocks:
    #    spell = parse_spell_block(block)
    #    if spell:
    #        spells.append(spell)
    #with open(out_json, 'w', encoding='utf-8') as f:
    #    json.dump(spells, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main("spell_descriptions.pdf", "data/spells_phb.json")