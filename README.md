# Bloom Filter

Space-efficient probabilistic data structure with configurable hash functions and false positive rate.

## What is a Bloom Filter?

A Bloom filter is a probabilistic data structure for membership testing. It can answer "is this item in the set?" with perfect accuracy for positives and a tunable false positive rate for negatives. It uses far less space than storing the entire set.

## Features

- Configurable bit array size to control false positive rate
- Multiple hash functions for collision spreading
- Custom hash function support
- False positive rate calculation
- Pythonic interface with "in" operator support
- Full test suite with 12+ test cases

## How It Works

1. Initialization: Create bit array of size N with K hash functions
2. Add: Hash element K times, set those bit positions to 1
3. Lookup: Hash element K times. If ALL positions are 1, might be in set. If ANY is 0, definitely not.

Trade-off: Never false negatives, but false positives are possible.

## Installation

Copy bloom_filter.py to your project.

## Usage

Basic example:

    from bloom_filter import BloomFilter
    bf = BloomFilter(size=1000, num_hashes=3)
    bf.add("apple")
    bf.add_many(["cherry", "date"])
    if "apple" in bf:
        print("Found")

Custom hash functions:

    bf = BloomFilter(size=1000, num_hashes=2, 
                     hash_functions=[hash1, hash2])

## Design Decisions

1. SHA256 for default hashing: High-quality cryptographic distribution
2. Configurable parameters: Size and num_hashes at construction
3. Custom hash support: Advanced users can provide specialized functions
4. No deletion: Standard Bloom filters don't support removal
5. Simple API: Follows Python conventions (add, contains, in operator)

## Testing

Run tests:

    python -m pytest test_bloom_filter.py
    python test_bloom_filter.py

Tests cover:
- Adding single and multiple items
- Membership checking
- False positive behavior
- Custom hash functions
- Invalid parameters
- False positive rate calculation
- Approximate item count

## Performance

- Space: O(M) where M is bit array size
- Add: O(K) where K is number of hash functions
- Lookup: O(K)
- False positive rate: Approximately (1 - e^(-KN/M))^K

## Use Cases

- Web crawling: Track visited URLs efficiently
- Caching: Pre-filter before expensive lookups
- Spell checking: Store valid words dictionary
- Privacy: Detect passwords in breach databases
- Distributed systems: Reduce network traffic
- Databases: First-pass filters before disk I/O

## Limitations

- No removal of items after adding
- False positives will occur based on parameters
- Size must be determined before use
- Cannot iterate over stored elements

## Applications

Real-world use: Google Chrome, Apache Cassandra, HBase, PostgreSQL

## License

MIT
