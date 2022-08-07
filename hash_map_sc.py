# Name: Geoff Miller
# OSU Email: millegeo@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/9/2022
# Description: Separate Chain class which implements the following methods for utilizing the class: empty_buckets,
#           put(), table_load(), clear(), contains_key(), get(), remove(), resize_table(), get_keys_and_values()
#           and find_mode()


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Method too add new key/value pair to the hash map. Takes a key and a value
        for parameters. Runs the hash function on the key for determining the index
        in the bucket that the value is associated with. Adds Key: value to index and
        returns None.
        """
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        linked_list = self._buckets.get_at_index(index)


        if linked_list.contains(key):
            linked_list.remove(key)
            linked_list.insert(key, value)
        else:
            linked_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Method that determines how many buckets are empty. Takes no parameters
        an returns the number of buckets that contain an empty SLL.
        """
        count = 0

        array = self._buckets

        for index in range(array.length()):
            if array.get_at_index(index).length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Method to return the load factor (ie. average size of each bucket.
        Takes no parameters and return load factor.
        """
        size = self._size
        buckets = self._buckets.length()

        return size/buckets

    def clear(self) -> None:
        """
        Method that clears all of the contents of the Hash Map to reset it to
        being empty.
        """

        self._buckets = DynamicArray()
        self._size = 0

        for index in range(0, self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Method that takes a capacity for its input and returns None. First determines
        if the new_capacity is prime. If it is then uses this capacity to re-map hash table
        to new capacity. Otherwise determines the next available prime to use and re-maps hash
        table.
        """
        if new_capacity < 1:
            return

        if self._is_prime(new_capacity):
            capacity = new_capacity
        else:
            capacity = self._next_prime(new_capacity)

        old_cap = self._capacity
        old_array = self._buckets

        self._capacity = capacity
        self.clear()

        for bucket in range(old_cap):
            if old_array.get_at_index(bucket).length() > 0:
                for linked_list in old_array.get_at_index(bucket):
                    self.put(linked_list.key, linked_list.value)


    def get(self, key: str) -> object:
        """
        Method to get a specified key in a hash map. Takes a key as input
        returns the value of the key if it is in the hash map else returns
        None.
        """
        hash_map = self._buckets

        hash = self._hash_function(key)
        index = hash % self._capacity

        if hash_map.get_at_index(index).contains(key):
            node = hash_map.get_at_index(index).contains(key)
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Method that iterates through the hash map and determines if the given key
        is defined. If yes returns True, else returns False.
        """
        if self.get(key) is not None:
            return True

        else:
            return False

    def remove(self, key: str) -> None:
        """
        Method to remove a key:value pair from the hashtable. Takes a key as
        parameter and removes that key from the SLL if it is present. Returns None.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity

        if self.contains_key(key):
            self._buckets.get_at_index(index).remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method that takes no parameters. It then iterates through the hash table and
        appends a tuple containing (key,value) of each node to a dynamic array. Returns
        the array.
        """
        array = DynamicArray()

        for ele in range(self._capacity):
            if self._buckets.get_at_index(ele).length() > 0:
                for node in self._buckets.get_at_index(ele):
                    array.append((node.key, node.value))

        return array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Method that takes a dynamic array for its parameter and returns a tuple containing the mode and frequency of
    the dynamic array. First creates a hash map with the key and value being the frequency of the key. Then iterates
    through the hashmap to determine which key is the mode and what frequency the key is repeated.
    """

    map = HashMap()

    for ele in range(da.length()):  #Create a hash map containing the key as the array value and frequency of repitiion for the value.
        key = da.get_at_index(ele)
        hash = hash_function_1(key)
        index = hash % map.get_capacity()
        if map.contains_key(key):
            value = map.get(key)
            value += 1
            map.put(key, value)
        else:
            map.put(key, 1)

    array = DynamicArray()          #Empty array for later return tuple.
    mode = None

    for ele in range(da.length()):  #Iterate through map and determine which keys are the mode. Add to array.
        key = da.get_at_index(ele)
        hash = hash_function_1(key)
        index = hash % map.get_capacity()

        if map.get(key):
            if mode is None:        #First index
                mode = map.get(key)
                array.append(key)
                map.remove(key)
            elif map.get(key) > mode:   #New mode/create new DA
                array = DynamicArray()
                mode = map.get(key)
                array.append(key)
                map.remove(key)
            elif map.get(key) == mode:  #Append string to DA frequency does not change.
                array.append(key)
                map.remove(key)

    return (array, mode)
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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
