# HashTable class using chaining

class ChainedHashTable:
    # constructor with capacity parameter. All buckets get an empty list
    def __init__(self,  initial_capacity=8):
        # initialize hash table with empty buckets.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Insert new item into hash table.
    def insert(self, key, item):
        # get bucket to put item.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if already present.
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if new key, insert item to end of bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # search for item with matching key.
    # returns item if found, otherwise None.
    def search(self, key):
        # hash key to get its respective bucket list.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list.
        for key_value in bucket_list:
            # find key value pair match in bucket.
            if key_value[0] == key:
                return key_value[1]
            # if no match, returns None.
            return None

    # remove item with matching key from hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if present.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0],kv[1]])