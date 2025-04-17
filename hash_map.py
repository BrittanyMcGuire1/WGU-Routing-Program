class HashTable:

    # Initialize the chaining hash table with an initial capacity that fits the amount of packages.
    #Time Complexity O(n)
    #Space Complexity O(n)
    def __init__(self, init_cap=45):
        self.capacity = init_cap
        self.table = []
        self.count = 0
        for i in range(init_cap):
            self.table.append([])

    #Loops through all buckets and shows the key-value pairs.
    #And adds it to table object
    # Time Complexity O(n)
    # Space Complexity O(n)
    def __str__(self):
        result = ""
        for bucket in self.table:
            for key, value in bucket:
                result += f"Key: {key}, Value: {value}\n"
        return result

    # Inserts key value pairs into the hash table
    # Time Complexity O(1) (If no collisions)
    # Space Complexity O(1)
    def insert(self, key, item):
        #Auto resize trigger
        if self.count / self.capacity > 0.75:
            self.resize()
        bucket_i = hash(key) % len(self.table)
        bucket_list = self.table[bucket_i]
        for kv_pair in bucket_list:
            if kv_pair[0] == key:
                kv_pair[1] = item
                return True
        new_key = [key, item]
        bucket_list.append(new_key)
        self.count += 1
        return True

    # Deletes key value pair by the key from the hash table
    # Time Complexity O(1)
    # Space Complexity O(1)
    def delete(self, key):
        bucket_index = hash(key) % len(self.table)
        bucket_list = self.table[bucket_index]

        for kv_pair in bucket_list:
            if kv_pair[0] == key:
                bucket_list.remove(kv_pair)

    # Resize function to handle collisions
    # Time Complexity O(n)
    # Space Complexity O(n)
    def resize(self):
        old_table = self.table
        new_capacity = len(self.table) * 2
        self.table = [[] for _ in range(new_capacity)]
        self.capacity = new_capacity

        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    # Searches values by Key from hash table
    # Time Complexity O(1)
    # Space Complexity O(1)
    def get(self, key):

        bucket_index = hash(key) % len(self.table)
        bucket_list = self.table[bucket_index]

        for kv_pair in bucket_list:
            if kv_pair[0] == key:
                return kv_pair[1]
        return None

    # Helper function
    # Time Complexity O(1)
    # Space Complexity O(1)
    def lookup(self, key):
        return self.get(key)