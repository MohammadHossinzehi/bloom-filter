import hashlib
from typing import Callable, List, Set

class BloomFilter:
    """Space-efficient probabilistic data structure for membership testing."""
    
    def __init__(self, size: int = 1000, num_hashes: int = 3, 
                 hash_functions: List[Callable] = None):
        """
        Initialize a Bloom filter.
        
        Args:
            size: Size of the bit array (higher = lower false positive rate)
            num_hashes: Number of hash functions to use
            hash_functions: Custom list of hash functions. If None, 
                          uses num_hashes of built-in hash functions
        """
        if size <= 0:
            raise ValueError("Size must be positive")
        if num_hashes <= 0:
            raise ValueError("Number of hashes must be positive")
            
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size
        
        if hash_functions:
            if len(hash_functions) != num_hashes:
                raise ValueError(f"Expected {num_hashes} hash functions, got {len(hash_functions)}")
            self.hash_functions = hash_functions
        else:
            self.hash_functions = [self._default_hash(i) for i in range(num_hashes)]
    
    def _default_hash(self, seed: int) -> Callable:
        """Create a default hash function with a given seed."""
        def hash_func(item: str) -> int:
            # Use hashlib with the seed to generate deterministic hash
            h = hashlib.sha256()
            h.update((str(seed) + str(item)).encode('utf-8'))
            return int(h.hexdigest(), 16) % self.size
        return hash_func
    
    def add(self, item: str) -> None:
        """Add an item to the Bloom filter."""
        for hash_func in self.hash_functions:
            index = hash_func(item)
            self.bit_array[index] = True
    
    def contains(self, item: str) -> bool:
        """Check if item might be in the set (may have false positives)."""
        for hash_func in self.hash_functions:
            index = hash_func(item)
            if not self.bit_array[index]:
                return False
        return True
    
    def add_many(self, items: List[str]) -> None:
        """Add multiple items to the filter."""
        for item in items:
            self.add(item)
    
    def false_positive_rate(self) -> float:
        """Calculate approximate false positive rate."""
        set_bits = sum(self.bit_array)
        if set_bits == 0:
            return 0.0
        return pow(set_bits / self.size, self.num_hashes)
    
    def __len__(self) -> int:
        """Return approximate number of elements (rough estimate)."""
        return sum(self.bit_array)
    
    def __contains__(self, item: str) -> bool:
        """Support 'in' operator."""
        return self.contains(item)
