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
            name=address['name'],
            street1=address['street1'],
            street2=address.get('street2', ''),
            city=address['city'],
            state=address['state'],
            zip=address['zip'],
            country=address.get('country', 'US')
        )

        if verified_address.verifications.delivery:
            return verified_address
    except easypost.Error as e:
        print(f"Error verifying address: {e}")
        return None

def main():
    verified_addresses = []

    # Load addresses from CSV file
    with open('addresses.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            address = {
                'name': row['name'],
                'street1': row['street1'],
                'city': row['city'],
                'state': row['state'],
                'zip': row['zip'],
            }
            verified_address = verify_address(address)
            if verified_address:
                verified_addresses.append(verified_address)
            else:
                return
            # Introduce a 300ms delay between requests
            time.sleep(0.3)

    # Write verified addresses to CSV file
    with open('verified_addresses.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['easypost_id','name','street1', 'city', 'state', 'zip', 'country', 'success','errors'])
        writer.writeheader()
        for address in verified_addresses:
            writer.writerow({
                'easypost_id':address.id,
                'name':address.name,
                'street1': address.street1,
                'city': address.city,
                'state': address.state,
                'zip': address.zip,
                'country': address.country,
                'success':address.verifications.delivery.success,
                'errors':address.verifications.delivery.errors[0].code if address.verifications.delivery.errors else "none"
            })

if __name__ == "__main__":
    main()
