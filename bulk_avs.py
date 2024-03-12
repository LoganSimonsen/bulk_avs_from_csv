import easypost
import csv
import time
from dotenv import dotenv_values

# Set your EasyPost API key
easypost.api_key = dotenv_values(".env")['TEST_API_KEY']

def verify_address(address):
    try:
        verified_address = easypost.Address.create(
            verify=[True],
            street1=address['street1'],
            street2=address.get('street2', ''),
            city=address['city'],
            state=address['state'],
            zip=address['zip'],
            country=address.get('country', 'US')
        )

        if verified_address.verifications.delivery.success:
            return verified_address
        else:
            return None
    except easypost.Error as e:
        print(f"Error verifying address: {e}")
        return None

def main():
    verified_addresses = []
    failed_addresses = []

    # Load addresses from CSV file
    with open('addresses.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            address = {
                'street1': row['street1'],
                'street2': row.get('street2', ''),
                'city': row['city'],
                'state': row['state'],
                'zip': row['zip'],
            }
            verified_address = verify_address(address)
            if verified_address:
                verified_addresses.append(verified_address)
            else:
                failed_addresses.append(address)

            # Introduce a 300ms delay between requests
            time.sleep(0.3)

    # Write successfully verified addresses to CSV file
    with open('verified_addresses.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['street1', 'street2', 'city', 'state', 'zip', 'country', 'easypost_id'])
        writer.writeheader()
        for address in verified_addresses:
            writer.writerow({
                'street1': address.street1,
                'street2': address.street2,
                'city': address.city,
                'state': address.state,
                'zip': address.zip,
                'country': address.country,
                'easypost_id':address.id
            })

    # Write failed addresses to CSV file
    with open('failed_addresses.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['street1', 'street2', 'city', 'state', 'zip', 'country'])
        writer.writeheader()
        for address in failed_addresses:
            writer.writerow(address)

if __name__ == "__main__":
    main()
