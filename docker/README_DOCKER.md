# Docker Usage Guide

This guide explains how to use Docker to run the Cybersecurity Datasets Downloader.

## 🐳 Quick Start with Docker

### Build the Docker Image

```bash
cd docker
docker build -t cybersec-downloader -f Dockerfile ..
```

### Run with Docker

```bash
# Run all phases
docker run -v $(pwd)/data:/data cybersec-downloader

# Run specific phase
docker run -v $(pwd)/data:/data cybersec-downloader python download_all.py --phase 1 --dir /data/cybersecurity_datasets

# Run with NVD API key for faster CVE downloads
docker run -v $(pwd)/data:/data -e NVD_API_KEY=your_api_key_here cybersec-downloader
```

## 🐳 Using Docker Compose

Docker Compose simplifies running the container with predefined settings.

### Basic Usage

```bash
cd docker
docker-compose up
```

### With API Key

Create a `.env` file in the `docker` directory:

```bash
NVD_API_KEY=your_api_key_here
```

Then run:

```bash
docker-compose up
```

### Run Specific Phase

```bash
docker-compose run downloader python download_all.py --phase 1 --dir /data/cybersecurity_datasets
```

### Run in Background

```bash
docker-compose up -d
```

### View Logs

```bash
docker-compose logs -f
```

### Stop and Remove

```bash
docker-compose down
```

## 📁 Volume Management

### Default Volume Location

By default, data is stored in `./data` directory relative to the `docker` folder.

### Custom Volume Location

Edit `docker-compose.yml`:

```yaml
volumes:
  - /path/to/your/data:/data
```

Or specify when running:

```bash
docker run -v /path/to/your/data:/data cybersec-downloader
```

### Check Downloaded Data

```bash
# List downloaded datasets
ls -lh ./data/cybersecurity_datasets/

# Check progress
docker run -v $(pwd)/data:/data cybersec-downloader python check_progress.py --dir /data/cybersecurity_datasets
```

## 🔧 Advanced Configuration

### Custom Base Directory

```bash
docker run -v $(pwd)/data:/data cybersec-downloader python download_all.py --dir /data/custom_location
```

### Interactive Shell

```bash
docker run -it -v $(pwd)/data:/data cybersec-downloader /bin/bash
```

### Run Multiple Phases in Sequence

```bash
docker run -v $(pwd)/data:/data cybersec-downloader sh -c "
  python download_all.py --phase 1 --dir /data/cybersecurity_datasets && \
  python download_all.py --phase 2 --dir /data/cybersecurity_datasets && \
  python download_all.py --phase 3 --dir /data/cybersecurity_datasets && \
  python download_all.py --phase 4 --dir /data/cybersecurity_datasets
"
```

## 🌐 Environment Variables

### Available Environment Variables

- `NVD_API_KEY` - API key for NVD (National Vulnerability Database)
- `DATA_DIR` - Base directory for datasets (default: `/data`)

### Setting Environment Variables

#### Using -e flag:

```bash
docker run -v $(pwd)/data:/data \
  -e NVD_API_KEY=your_key \
  -e DATA_DIR=/data \
  cybersec-downloader
```

#### Using .env file with Docker Compose:

Create `.env` file:

```env
NVD_API_KEY=your_api_key_here
DATA_DIR=/data
```

## 🔍 Troubleshooting

### Permission Issues

If you encounter permission issues with the mounted volume:

```bash
# Fix ownership
sudo chown -R 1000:1000 ./data
```

Or run as root (not recommended for production):

```bash
docker run --user root -v $(pwd)/data:/data cybersec-downloader
```

### Out of Disk Space

The datasets can be large. Ensure you have enough disk space:

```bash
# Check available space
df -h

# Monitor container disk usage
docker system df
```

### Network Issues

If downloads fail due to network issues:

```bash
# Increase Docker timeout
docker run --network host -v $(pwd)/data:/data cybersec-downloader
```

### Container Won't Start

Check logs:

```bash
docker logs cybersec-datasets-downloader

# Or with Docker Compose
docker-compose logs
```

## 🎯 Use Cases

### Continuous Updates

Run periodically to update datasets:

```bash
# Add to crontab to run weekly
0 0 * * 0 cd /path/to/docker && docker-compose up >> /var/log/cybersec-downloader.log 2>&1
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Download datasets
  run: |
    docker build -t cybersec-downloader -f docker/Dockerfile .
    docker run -v $PWD/datasets:/data cybersec-downloader
```

### Multiple Projects

Use different volumes for different projects:

```bash
# Project A
docker run -v $PWD/project-a-data:/data cybersec-downloader

# Project B
docker run -v $PWD/project-b-data:/data cybersec-downloader
```

## 🚀 Performance Tips

1. **Use SSD** - Mount volumes on SSD for better performance
2. **Allocate memory** - Give Docker more RAM (Settings > Resources)
3. **API key** - Use NVD API key for 10x faster CVE downloads
4. **Parallel phases** - Run different phases in separate containers

## 🧹 Cleanup

### Remove Container

```bash
docker rm cybersec-datasets-downloader
```

### Remove Image

```bash
docker rmi cybersec-downloader
```

### Clean All Docker Resources

```bash
docker system prune -a
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Main README](../README.md)

## 🤝 Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.
