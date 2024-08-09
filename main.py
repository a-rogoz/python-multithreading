import threading
import requests


# List of URLs to download
urls = [
    '',
    '',
    '',
]

# Lock for file writing
file_lock = threading.Lock()


# Function to download a file from a given URL
def download_file(url):
    try:
        # Print the thread ID and the URL of the file being downloaded
        thread_id = threading.get_ident()
        print(f"Thread {thread_id} is handling {url}...")

        filename = url.split("/")[-1]
        print(f"Downloading {filename}...")
        response = requests.get(url)

        if response.status_code == 200:
            # Acquire the lock before writing to the file
            with file_lock:
                with open(filename, "wb") as file:
                    file.write(response.content)
            print(f"{filename} downloaded successfully.")
        else:
            print(f"Failed to downnload {filename}.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


# Function to create and start threads for downloading files
def download_files(urls, max_threads):
    threads = []
    active_threads = threading.active_count()
    for url in urls:
        # Check if the maximum number of threads has been reached
        if active_threads >= max_threads:
            break

        thread = threading.Thread(target=download_file, args=(url,))
        threads.append(thread)
        thread.start()
        active_threads += 1

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


# Main function
def main():
    # Maximum number of threads to start
    max_threads = 3
    # Download files concurrently using multithreading
    download_files(urls, max_threads)


if __name__ == "__main__":
    main()