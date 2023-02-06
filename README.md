# lxd-python

Python API wrapper for LXD. This library is a work in progress and is not yet ready for production use.

## Testing

To run the tests, you need to have a running LXD instance running on your machine. You can either use the snap package or install LXD from the official website.

Tests will connect to `/var/lib/lxd/unix.socket`.

Once you have LXD installed, you can run the tests with:

```bash
poetry run pytest -vvvvvv --exitfirst --random-order --random-order-bucket=global
```

## Contributing

Contributions are welcome! Please open an issue or a pull request. If you are planning to make a large change, please open an issue or contact me first.

## Contact

- Email: tlovinator@gmail.com
- Discord: TheLovinator#9276
- Send an issue: [lxd-python/issues](https://github.com/TheLovinator1/lxd-python/issues)
