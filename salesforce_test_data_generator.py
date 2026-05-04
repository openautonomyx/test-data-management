#!/usr/bin/env python3
"""
Salesforce Sales Cloud Test Data Generator
Generates realistic test data for Salesforce objects with relationships
"""

import argparse
import csv
import json
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Sample data pools for realistic generation
FIRST_NAMES = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Jessica", "James", "Jennifer",
               "William", "Amanda", "Richard", "Nicole", "Joseph", "Lisa", "Thomas", "Karen", "Christopher", "Nancy",
               "Daniel", "Maria", "Matthew", "Sandra", "Mark", "Patricia", "Donald", "Diane", "Steven", "Julie"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
              "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]

COMPANY_NAMES = ["Acme Corp", "TechVision Inc", "Global Solutions LLC", "Enterprise Systems", "Digital Innovations",
                 "CloudFirst Technologies", "DataStream Analytics", "SecureNet Solutions", "InnovatePlus", "PrimeTech Group",
                 "Apex Industries", "Velocity Systems", "Quantum Computing", "Future Tech Labs", "Smart Solutions Inc"]

INDUSTRIES = ["Technology", "Finance", "Healthcare", "Retail", "Manufacturing", "Telecommunications", "Energy",
              "Transportation", "Education", "Media"]

CITIES = ["San Francisco", "New York", "Los Angeles", "Chicago", "Boston", "Seattle", "Austin", "Denver", "Miami", "Atlanta",
          "London", "Paris", "Tokyo", "Sydney", "Toronto", "Berlin", "Amsterdam", "Singapore", "Hong Kong", "Dubai"]

STATES = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI", "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "LA", "CO"]

COUNTRIES = ["United States", "United Kingdom", "Canada", "Germany", "France", "Japan", "Australia", "India", "Brazil", "Mexico"]

TITLES = ["Sales Manager", "Account Executive", "Sales Development Rep", "VP of Sales", "Director of Sales",
          "Chief Technology Officer", "Chief Financial Officer", "Product Manager", "Marketing Manager", "Operations Manager",
          "Business Analyst", "Project Manager", "Systems Administrator", "IT Director", "Financial Analyst"]

OPPORTUNITY_STAGES = ["Prospecting", "Qualification", "Needs Analysis", "Value Proposition", "Negotiation", "Closed Won", "Closed Lost"]

QUOTE_STATUS = ["Draft", "Sent", "Accepted", "Rejected", "Expired"]

ORDER_STATUS = ["Draft", "Activated", "Cancelled"]


class SalesforceTestDataGenerator:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self.account_ids: List[str] = []
        self.contact_ids: List[str] = []
        self.opportunity_ids: List[str] = []
        self.quote_ids: List[str] = []
        self.order_ids: List[str] = []

    def generate_id(self, prefix: str) -> str:
        """Generate a realistic Salesforce ID."""
        return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    def generate_email(self, first_name: str, last_name: str, company_name: str) -> str:
        """Generate realistic email."""
        company_domain = company_name.lower().replace(" ", "").replace(".", "") + ".com"
        return f"{first_name.lower()}.{last_name.lower()}@{company_domain}"

    def generate_phone(self) -> str:
        """Generate realistic US phone number."""
        return f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"

    def generate_website(self, company_name: str) -> str:
        """Generate website from company name."""
        domain = company_name.lower().replace(" ", "").replace(".", "")
        return f"https://www.{domain}.com"

    def generate_accounts(self, count: int) -> List[Dict]:
        """Generate Account records."""
        accounts = []
        for _ in range(count):
            account_id = self.generate_id("001")
            self.account_ids.append(account_id)

            company_name = random.choice(COMPANY_NAMES) + f" {random.randint(1, 9999)}"

            account = {
                "Id": account_id,
                "Name": company_name,
                "BillingStreet": f"{random.randint(100, 9999)} Main Street",
                "BillingCity": random.choice(CITIES),
                "BillingState": random.choice(STATES),
                "BillingCountry": random.choice(COUNTRIES),
                "BillingPostalCode": f"{random.randint(10000, 99999)}",
                "Phone": self.generate_phone(),
                "Website": self.generate_website(company_name),
                "Industry": random.choice(INDUSTRIES),
                "AnnualRevenue": random.choice([500000, 1000000, 5000000, 10000000, 50000000, 100000000, 500000000]),
                "NumberOfEmployees": random.choice([10, 50, 100, 500, 1000, 5000, 10000]),
                "Description": f"Account created for testing. {random.choice(INDUSTRIES)} sector.",
            }
            accounts.append(account)

        return accounts

    def generate_contacts(self, contacts_per_account: Tuple[int, int] = (2, 4)) -> List[Dict]:
        """Generate Contact records linked to accounts."""
        contacts = []
        for account_id in self.account_ids:
            count = random.randint(contacts_per_account[0], contacts_per_account[1])
            for _ in range(count):
                contact_id = self.generate_id("003")
                self.contact_ids.append(contact_id)

                first_name = random.choice(FIRST_NAMES)
                last_name = random.choice(LAST_NAMES)

                contact = {
                    "Id": contact_id,
                    "FirstName": first_name,
                    "LastName": last_name,
                    "Email": self.generate_email(first_name, last_name, account_id),
                    "Phone": self.generate_phone(),
                    "MobilePhone": self.generate_phone(),
                    "AccountId": account_id,
                    "Title": random.choice(TITLES),
                    "Department": random.choice(["Sales", "Engineering", "Marketing", "Finance", "Operations"]),
                    "MailingCity": random.choice(CITIES),
                    "MailingState": random.choice(STATES),
                    "MailingCountry": random.choice(COUNTRIES),
                    "Description": "Contact created for testing.",
                }
                contacts.append(contact)

        return contacts

    def generate_opportunities(self, opps_per_account: Tuple[int, int] = (1, 3)) -> List[Dict]:
        """Generate Opportunity records linked to accounts."""
        opportunities = []
        for account_id in self.account_ids:
            count = random.randint(opps_per_account[0], opps_per_account[1])
            for j in range(count):
                opp_id = self.generate_id("006")
                self.opportunity_ids.append(opp_id)

                stage = random.choice(OPPORTUNITY_STAGES)
                amount = random.randint(5, 500) * 1000
                close_date = datetime.now() + timedelta(days=random.randint(30, 180))

                stage_probability = {
                    "Prospecting": 10,
                    "Qualification": 20,
                    "Needs Analysis": 30,
                    "Value Proposition": 40,
                    "Negotiation": 60,
                    "Closed Won": 100,
                    "Closed Lost": 0,
                }

                opp = {
                    "Id": opp_id,
                    "Name": f"{account_id} - Opportunity {j + 1}",
                    "AccountId": account_id,
                    "StageName": stage,
                    "Amount": amount,
                    "Probability": stage_probability.get(stage, 50),
                    "CloseDate": close_date.strftime("%Y-%m-%d"),
                    "Description": f"Test opportunity for account. Stage: {stage}",
                    "Type": random.choice(["New Business", "Existing Business", "Expansion"]),
                }
                opportunities.append(opp)

        return opportunities

    def generate_quotes(self, quote_ratio: float = 0.6) -> List[Dict]:
        """Generate Quote records linked to opportunities."""
        quotes = []
        selected_opps = random.sample(self.opportunity_ids, int(len(self.opportunity_ids) * quote_ratio))

        for i, opp_id in enumerate(selected_opps):
            quote_id = self.generate_id("701")
            self.quote_ids.append(quote_id)

            quote = {
                "Id": quote_id,
                "Name": f"Quote {i + 1}",
                "OpportunityId": opp_id,
                "QuoteNumber": f"Q-{random.randint(10000, 99999)}",
                "Status": random.choice(QUOTE_STATUS),
                "Total": random.randint(5, 500) * 1000,
                "ExpirationDate": (datetime.now() + timedelta(days=random.randint(14, 90))).strftime("%Y-%m-%d"),
                "Description": "Test quote created for testing",
            }
            quotes.append(quote)

        return quotes

    def generate_orders(self, order_ratio: float = 0.7) -> List[Dict]:
        """Generate Order records."""
        orders = []
        selected_quotes = random.sample(self.quote_ids, int(len(self.quote_ids) * order_ratio)) if self.quote_ids else []

        for quote_id in selected_quotes:
            order_id = self.generate_id("801")
            self.order_ids.append(order_id)

            order = {
                "Id": order_id,
                "OrderNumber": f"ORD-{random.randint(100000, 999999)}",
                "Status": random.choice(ORDER_STATUS),
                "EffectiveDate": datetime.now().strftime("%Y-%m-%d"),
                "TotalAmount": random.randint(5, 500) * 1000,
                "Description": "Test order created for testing",
            }
            orders.append(order)

        return orders

    def generate_order_items(self, items_per_order: Tuple[int, int] = (2, 5)) -> List[Dict]:
        """Generate Order Item records."""
        items = []
        for order_id in self.order_ids:
            count = random.randint(items_per_order[0], items_per_order[1])
            for i in range(count):
                item = {
                    "OrderId": order_id,
                    "Description": f"Product/Service {i + 1}",
                    "Quantity": random.randint(1, 100),
                    "UnitPrice": random.choice([100, 500, 1000, 5000, 10000]),
                    "ListPrice": random.choice([100, 500, 1000, 5000, 10000]),
                    "ServiceDate": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
                }
                items.append(item)

        return items

    def generate_all(self, account_count: int = 50, include_contacts: bool = True,
                     include_opportunities: bool = True, include_quotes: bool = True,
                     include_orders: bool = True) -> Dict:
        """Generate all data."""
        data = {}

        print(f"Generating {account_count} Accounts...")
        data["Accounts"] = self.generate_accounts(account_count)

        if include_contacts:
            print("Generating Contacts...")
            data["Contacts"] = self.generate_contacts()

        if include_opportunities:
            print("Generating Opportunities...")
            data["Opportunities"] = self.generate_opportunities()

        if include_quotes:
            print("Generating Quotes...")
            data["Quotes"] = self.generate_quotes()

        if include_orders:
            print("Generating Orders...")
            data["Orders"] = self.generate_orders()
            print("Generating Order Items...")
            data["OrderItems"] = self.generate_order_items()

        return data


def save_as_csv(data: Dict, output_dir: str = "."):
    """Save data to CSV files."""
    import os

    os.makedirs(output_dir, exist_ok=True)

    for object_name, records in data.items():
        if not records:
            continue

        filename = f"{output_dir}/{object_name}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
        print(f"Saved {len(records)} {object_name} to {filename}")


def save_as_json(data: Dict, output_file: str = "salesforce_test_data.json"):
    """Save data to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Saved all data to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Salesforce test data")
    parser.add_argument("--accounts", type=int, default=50, help="Number of accounts to generate")
    parser.add_argument("--format", choices=["csv", "json", "both"], default="csv", help="Output format")
    parser.add_argument("--output", type=str, default=".", help="Output directory/file")
    parser.add_argument("--no-contacts", action="store_true", help="Skip generating contacts")
    parser.add_argument("--no-opportunities", action="store_true", help="Skip generating opportunities")
    parser.add_argument("--no-quotes", action="store_true", help="Skip generating quotes")
    parser.add_argument("--no-orders", action="store_true", help="Skip generating orders")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")

    args = parser.parse_args()

    generator = SalesforceTestDataGenerator(seed=args.seed)
    data = generator.generate_all(
        account_count=args.accounts,
        include_contacts=not args.no_contacts,
        include_opportunities=not args.no_opportunities,
        include_quotes=not args.no_quotes,
        include_orders=not args.no_orders,
    )

    if args.format in ["csv", "both"]:
        save_as_csv(data, args.output)

    if args.format in ["json", "both"]:
        output_file = args.output if args.format == "json" else f"{args.output}/salesforce_test_data.json"
        save_as_json(data, output_file)
