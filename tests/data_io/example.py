leafs = [
    (123, True),
    (71254, False),
    (42386, True),
]

json_dump = """
{
    "format": "standard-v1",
    "tree": [
        "0x045578d5e654c3f10fecce520b17f5b8073630bf780db850721b1a8a5df3b839",
        "0x9385965ba65029c2cbdb3782f35b755a76788ef236602b98118ef535cca36e5c",
        "0xee7349a2ed7003d5da5bcfdc43253f4a7b757d72ab681f3178469b73087ac3e7",
        "0x8b1d412fe317e16a1c98414d61c95cd2e44ba6b16907e90c2b0035cf6261d01d",
        "0x39ee1707f21ec11bac8c0d42538c09f71c0fe3ceb0a2f6be012c2769a714af3d",
    ],
    "values": [
        {"value": [123, True], "treeIndex": 2},
        {"value": [71254, False], "treeIndex": 4},
        {"value": [42386, True], "treeIndex": 3},
    ],
    "leafEncoding": ["int256", "bool"],
}
"""
