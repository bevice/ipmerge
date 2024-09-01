Merge files from stdin into subnets

Example: 

```bash
$ echo -e "192.168.0.1\n192.168.1.2" | python ipmerge.py --max-prefix=22
192.168.0.0/23
```
