Familiarize yourself with redis commands `RPUSH`, `LPUSH`, `LRANGE`, etc.

In this task, we will define a `call_history` decorator to store the history of inputs and outputs for a particular function.

Everytime the original function will be called, we will add its input parameters to one list in redis, and store its output into another list.

In `call_history`, use the decorated function’s qualified name and append `":inputs"` and `":outputs"` to create input and output list keys, respectively.

`call_history` has a single parameter named `method` that is a `Callable` and returns a `Callable`.

In the new function that the decorator will return, use `rpush` to append the input arguments. Remember that Redis can only store strings, bytes and numbers. Therefore, we can simply use `str(args)` to normalize. We can ignore potential `kwargs` for now.

Execute the wrapped function to retrieve the output. Store the output using `rpush` in the `"...:outputs"` list, then return the output.

Decorate `Cache.store` with `call_history`.

```
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

bob@dylan:~$ ./main.py
04f8dcaa-d354-4221-87f3-4923393a25ad
a160a8a8-06dc-4934-8e95-df0cb839644b
15a8fd87-1f55-4059-86aa-9d1a0d4f2aea
inputs: [b"('first',)", b"('secont',)", b"('third',)"]
outputs: [b'04f8dcaa-d354-4221-87f3-4923393a25ad', b'a160a8a8-06dc-4934-8e95-df0cb839644b', b'15a8fd87-1f55-4059-86aa-9d1a0d4f2aea']
bob@dylan:~$ 
```