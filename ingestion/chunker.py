from copy import deepcopy


def init_hierarchy_state():
    return {
        "chapter_index": 0,
        "chapter_title": None,
        "chapter_number_raw": None,
        "subchapter": None,
        "topic": None,
        "subtopic": None,
        "section": None,
    }


def update_hierarchy(state, block_type, text):
    if block_type == "chapter":
        state["chapter_index"] += 1
        state["chapter_title"] = text
        state["chapter_number_raw"] = (
            text.split()[1] if text.lower().startswith("chapter") else None
        )

        # reset lower levels
        state["subchapter"] = None
        state["topic"] = None
        state["subtopic"] = None
        state["section"] = None

    elif block_type == "topic":
        state["topic"] = text
        state["subtopic"] = None
        state["section"] = None

    elif block_type == "subtopic":
        state["subtopic"] = text
        state["section"] = None

    return state


def create_chunk(text_buffer, state, page_number):
    return {
        "text": " ".join(text_buffer).strip(),
        "metadata": {
            **deepcopy(state),
            "content_type": "text",
            "page_number": page_number,
        },
    }


def build_chunks(extracted_blocks):
    """
    Build hierarchy-aware text chunks from extracted PDF blocks.
    """
    state = init_hierarchy_state()
    chunks = []
    buffer = []
    buffer_page = None

    for block in extracted_blocks:
        text = block["text"]
        block_type = block["block_type"]
        page_number = block["page_number"]

        # If heading encountered, flush previous buffer
        if block_type in {"chapter", "topic", "subtopic"}:
            if buffer:
                chunks.append(
                    create_chunk(buffer, state, buffer_page)
                )
                buffer = []
                buffer_page = None

            state = update_hierarchy(state, block_type, text)
            continue

        # Body text accumulation
        if block_type == "body":
            if buffer_page is None:
                buffer_page = page_number
            buffer.append(text)

    # Flush last buffer
    if buffer:
        chunks.append(
            create_chunk(buffer, state, buffer_page)
        )

    return chunks
