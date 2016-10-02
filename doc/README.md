# Noded JSON Response Documentation

Noded exports various system and job information to an instance of Redis every
30 seconds.  The information is packaged as JSON, but stored in Redis as a
single string.  This was done to reduce the number of overall calls to Redis.

The **jobs** object in Redis responses will only exist if one or more jobs are
running on a given node.

## Response

```
{
    "jobs": {
        "14429477": {
            "active_threads": 2,
            "cpu_and_procs": {
                "0": [
                    [
                        "physphasn",
                        "R"
                    ]
                ],
                "16": [
                    [
                        "physphasn",
                        "R"
                    ]
                ]
            },
            "mem_alloc": "34359738368",
            "mem_usage": "7832281088",
            "overloaded": false,
            "user": "giovanni"
        },
    "last_updated": 1455302191.680521,
    "load": 15.64,
    "nodename": "c0034",
    "nodenum": 34, 
    "overloaded": false,
    "total_logical_cpus": 32, 
    "total_memory": 135290150912,
    "total_memory_used_percent": 17, 
    "total_swap": 2147479552,
    "total_swap_used_percent": 0
}
```

## Response Fields

| Name          | Type     | Description |
| --------      | -------- | ----------- |
| jobs          | dictionary | key: jobid, value: dictionary of job information (see [Jobs Object](#jobs-object)) |
| last_update   | float        | Timestamp in epoch (with microseconds) when this data was sent to Redis from the node |
| load       | int    | System load |
| nodename   | string | Hostname of this compute node |
| nodenum    | int    | Compute node number |
| overloaded | bool   | Whether this node has one or more overloaded jobs |
| total_logical_cpus        | int | Total number of logical CPUs on this node (includes HyperThreads) |
| total_memory              | int | Total size of system memory in bytes |
| total_memory_used_percent | int | Total memory used as a percentage of total_memory |
| total_swap                | int | Total size of system swap in bytes |
| total_swap_used_percent   | int | Total swap used as a percentage of total_swap |

## Jobs Object

```
{
    "jobs": {
        "14429477": {
            "active_threads": 2,
            "cpu_and_procs": {
                "0": [
                    [
                        "physphasn",
                        "R"
                    ]
                ],
                "16": [
                    [
                        "physphasn",
                        "R"
                    ]
                ]
            },
            "mem_alloc": "34359738368",
            "mem_usage": "7832281088",
            "overloaded": false,
            "user": "giovanni"
        }   
    }
}
```

| Name           | Type     | Description |
| --------       | -------- | ----------- |
| active_threads | int | Number of threads in the Running, Runnable or Disk Sleep states |
| cpu_and_procs  | dictionary | key: Allocated CPU, value: list of lists (see [CPU and Procs Object](#cpu-and-procs-object)) |
| mem_alloc  | string | Memory allocated to all threads for this jobid in bytes |
| mem_usage  | string | Memory used by all threads for this jobid in bytes |
| overloaded | bool | Whether active_threads > number of allocated CPUs for at least 2 minutes (4 Noded loops = 4 * 30 secs) |
| user       | string | Owner of this jobid |

## CPU and Procs Object


The cpu_and_procs object is a dictionary, with CPU IDs as the keys and list of lists as the values.
```
{
"cpu_and_procs": {
                  "0": [ ["physphasn", "R"] ],
                  "16": [ ["physphasn", "R"] ]
                 }
}
```

The **length** of the cpu_and_procs object equals the number of allocated CPUs for a given jobid.

```python
>>> len(cpus_and_procs)
2
>>>
```

The **length** of a CPU ID's list equals number of active threads on that given CPU.

```python
>>> len(cpu_and_procs["16"])
1
>>>
```

Each nested list references a single thread.  
Index 0 = name of process/thread
Index 1 = CPU state (R: Running, D: Disk Sleep)

```python
>>> cpu_and_procs["16"][0][0]
'physphasn'
>>> cpu_and_procs["16"][0][1]
'R'
>>> 
```

**Note:** I may change this to a NamedTuple which will not break backwards
compatibility, as tuples can be referenced by index, but can make access a
little easier and more readable.
