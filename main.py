import erq
import static

def main():
    # URL and file paths
    url = 'https://www.javatpoint.com/'
    filename = 'index.html'
    bucket_name = 'bucketdate'
    object_key = 'index.html'
    file_path = filename

    # Fetch HTML content and save to file
    erq.fetch_and_save_html(url, filename)

    # Set up S3 bucket and upload file
    static.setup_bucket(bucket_name, object_key, file_path)

if __name__ == '__main__':
   main()
