import unittest
from bloom_filter import BloomFilter

class TestBloomFilter(unittest.TestCase):
    """Test cases for BloomFilter class."""
    
    def setUp(self):
        """Create a fresh filter for each test."""
        self.filter = BloomFilter(size=100, num_hashes=3)
    
    def test_add_and_contains_single_item(self):
        """Test adding and checking a single item."""
        self.filter.add("hello")
        self.assertTrue("hello" in self.filter)
    
    def test_multiple_items(self):
        """Test adding and checking multiple items."""
        items = ["apple", "banana", "cherry", "date"]
        self.filter.add_many(items)
        
        for item in items:
            self.assertIn(item, self.filter)
    
    def test_not_contains_item(self):
        """Test that items not added are correctly identified as absent."""
        self.filter.add("world")
        self.assertNotIn("universe", self.filter)
    
    def test_false_positives_possible(self):
        """Document that false positives are possible."""
        # Add one item
        self.filter.add("test")
        self.assertTrue("test" in self.filter)
        
        # Many non-existent items might return True due to hash collisions
        # This is a probabilistic data structure, so we just document behavior
    
    def test_add_many_convenience_method(self):
        """Test the add_many convenience method."""
        items = ["one", "two", "three"]
        self.filter.add_many(items)
        
        for item in items:
            self.assertIn(item, self.filter)
    
    def test_false_positive_rate(self):
        """Test false positive rate calculation."""
        rate = self.filter.false_positive_rate()
        self.assertGreaterEqual(rate, 0.0)
        self.assertLessEqual(rate, 1.0)
        
        # Add some items
        self.filter.add_many(["a", "b", "c"])
        rate_after = self.filter.false_positive_rate()
        # Rate should increase with more items
        self.assertGreater(rate_after, rate)
    
    def test_len_approximate(self):
        """Test approximate count of bits set."""
        count_before = len(self.filter)
        self.filter.add_many(["x", "y", "z"])
        count_after = len(self.filter)
        # Count should increase (though not exactly by 3)
        self.assertGreater(count_after, count_before)
    
    def test_invalid_size(self):
        """Test that invalid size raises ValueError."""
        with self.assertRaises(ValueError):
            BloomFilter(size=0)
        
        with self.assertRaises(ValueError):
            BloomFilter(size=-5)
    
    def test_invalid_num_hashes(self):
        """Test that invalid num_hashes raises ValueError."""
        with self.assertRaises(ValueError):
            BloomFilter(num_hashes=0)
        
        with self.assertRaises(ValueError):
            BloomFilter(num_hashes=-1)
    
    def test_custom_hash_functions(self):
        """Test using custom hash functions."""
        def hash1(item: str) -> int:
            return hash(item) % 100
        
        def hash2(item: str) -> int:
            return hash(item + "seed") % 100
        
        bf = BloomFilter(size=100, num_hashes=2, 
                        hash_functions=[hash1, hash2])
        
        bf.add("test")
        self.assertIn("test", bf)
    
    def test_mismatch_hash_functions_count(self):
        """Test that hash function count must match num_hashes."""
        def hash_func(item):
            return 0
        
        with self.assertRaises(ValueError):
            BloomFilter(size=100, num_hashes=3, 
                       hash_functions=[hash_func])

if __name__ == "__main__":
    unittest.main()
