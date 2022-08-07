# Name: Geoff Miller
# OSU Email: millegeo@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/9/2022
# Description: Class for open addressing hash table that uses Quadratic Probing. Methods defined
#           are put(), get(), remove(), contains_key(), clear(), empty_buckets(), resize_table()
#           table_load(), and get_keys()


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method to put a key:value into the hash map. Takes a key and a value for parameters.
        Runs hashmap function on key to determine index. If index is not None runs through a
        quadratic probing sequence to determine next available index. Returns None.
        """

        if self.table_load() >= 0.5:
            self.resize_table((self._capacity)*2)

        entry = HashEntry(key, value)
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        initial_index = index
        probe = 1

        if self._buckets.get_at_index(index) is None:
            self._buckets.set_at_index(index, entry)
        else:
            while self._buckets.get_at_index(index) is not None and not self._buckets.get_at_index(index).is_tombstone:
                if entry.key == self._buckets.get_at_index(index).key:
                    self._buckets.set_at_index(index, entry)
                    return
                index = (initial_index + probe**2) % self._buckets.length()
                probe += 1

            self._buckets.set_at_index(index, entry)

        self._size += 1

    def table_load(self) -> float:
        """
        Method to return the load factor (ie. average size of each bucket.
        Takes no parameters and return load factor.
        """
        size = self._size
        buckets = self._buckets.length()

        return size / buckets

    def empty_buckets(self) -> int:
        """
        Method that takes no parameters. Iterates through the hash table and
        determines which buckets are empty. Returns the number of buckets that
        are empty.
        """
        count = 0

        for ele in range(self._buckets.length()):
            if self._buckets.get_at_index(ele) is None:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Method that resizes the hash table based on the capacity that is given as a parameter.
        Rehashes all key:value pairs after the capacity resize. Ensures that the capacity is a prime
        number. Returns None.
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1 or new_capacity < self._size:
            return

        if self._is_prime(new_capacity):
            capacity = new_capacity
        else:
            capacity = self._next_prime(new_capacity)

        old_cap = self._capacity
        old_array = self._buckets

        self._buckets = DynamicArray()
        self._capacity = capacity

        for ele in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

        for ele in range(old_cap):
            if old_array.get_at_index(ele) is not None:
                key = old_array.get_at_index(ele).key
                value = old_array.get_at_index(ele).value
                self.put(key,value)

    def get(self, key: str) -> object:
        """
        Method that obtains the value associated with the given key. Iterates
        through the possible indexes until key mathes. If it is not in hash table,
        returns None else returns the value.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        initial_index = index
        probe = 1

        while self._buckets.get_at_index(index) is not None and not self._buckets.get_at_index(index).is_tombstone:
            if key == self._buckets.get_at_index(index).key:
                return self._buckets.get_at_index(index).value
            index = (initial_index + probe ** 2) % self._buckets.length()
            probe += 1

    def contains_key(self, key: str) -> bool:
        """
        Method that takes a key for a parameter, if the key is defined in the
        hash table returns True, otherwise returns false.
        """
        if self.get(key) is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Method that effictively removes a key:value from the hash table. If the value
        is in the table it will set the hash entry tombstone to True. Returns None.
        """

        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        initial_index = index
        probe = 1

        while self._buckets.get_at_index(index) is not None:
            if key == self._buckets.get_at_index(index).key and not self._buckets.get_at_index(index).is_tombstone:
                self._buckets.get_at_index(index).is_tombstone = True
                self._size -= 1
            index = (initial_index + probe ** 2) % self._buckets.length()
            probe += 1

    def clear(self) -> None:
        """
        Method that clears the hash table. Takes no parameters, sets buckets to
        an empty dynamic array and appends None to the array until capacity is reached.
        Returns None
        """
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method that takes no parameters. Returns a DynamicArray that contains tuples
        of all key:value pairs in the hash table.
        """
        array = DynamicArray()

        for ele in range(self._capacity):
            if self._buckets.get_at_index(ele) is not None and not self._buckets.get_at_index(ele).is_tombstone:
                key = self._buckets.get_at_index(ele).key
                value = self._buckets.get_at_index(ele).value
                array.append((key,value))

        return array

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
