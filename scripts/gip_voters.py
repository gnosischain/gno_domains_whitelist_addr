import requests
import pandas as pd
import backoff
from io import StringIO
import sys
import os

def get_GIP_ids(timestamp_cutoff):
    url = 'https://hub.snapshot.org/graphql'
    payload = {
        "operationName": "Proposals",
        "variables": {
            "first": 1000, # Number gig enough to cover all GIPs
            "skip": 0,
            "space_in": ["gnosis.eth"],
            "state": "all",
            "title_contains": "",
            "flagged": False
        },
        "query": """query Proposals(
                    $first: Int!, 
                    $skip: Int!, 
                    $state: String!, 
                    $space: String, 
                    $space_in: [String], 
                    $author_in: [String], 
                    $title_contains: String, 
                    $space_verified: Boolean, 
                    $flagged: Boolean) {
            proposals(
            first: $first, 
            skip: $skip, 
            where: {
                space: $space, 
                state: $state, 
                space_in: $space_in, 
                author_in: $author_in, 
                title_contains: $title_contains, 
                space_verified: $space_verified, 
                flagged: $flagged
                }
            ) {
                id
                ,created
            }
        }"""
    }

    response = requests.post(url, json=payload)
    proposals = response.json()['data']['proposals']

    df_proposals = pd.DataFrame(proposals)
    proposals_ids = df_proposals[df_proposals['created'] <= timestamp_cutoff]['id'].values

    return proposals_ids

   

# Retry decorator to handle retries
@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def get_votes(proposal_id):
    url_votes = f'https://sh5.co/api/votes/{proposal_id}'
    response = requests.post(url_votes)
    if response.status_code == 200:
        return response
    else:
        response.raise_for_status()

def get_voting_addresses(proposals_ids):
    df_vote_addresses = pd.DataFrame(columns=['address'])
    for proposal_id in proposals_ids:
        print("Proposal id: ",proposal_id)
        try:
            response = get_votes(proposal_id)
            data = StringIO(response.text)
            df = pd.read_csv(data)
            df_vote_addresses = pd.concat([df['address'], df_vote_addresses])
        except requests.exceptions.HTTPError as e:
            print(f"Failed to retrieve data for proposal {proposal_id}, status code: {response.status_code}")
    return df_vote_addresses

def main():
    timestamp_cutoff = 1720980000  # 2024/07/14 18:00 UTC
    proposals_ids = get_GIP_ids(timestamp_cutoff)
    df_vote_addresses = get_voting_addresses(proposals_ids)

    # Path to the parent directory's data folder
    data_folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)  

    csv_filename = os.path.join(data_folder_path, f'addresses_gip_voters.csv')

    df_vote_addresses['address'].to_csv(csv_filename, index=False)

    print(f"CSV file has been created: {csv_filename}")

if __name__ == "__main__":
    main()