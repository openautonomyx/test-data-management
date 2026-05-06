#!/usr/bin/env python3
"""Salesforce Sales Cloud Test Data Generator."""

import argparse
import csv
import json
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence, Tuple

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
STAGE_PROBABILITY = {
    "Prospecting": 10,
    "Qualification": 20,
    "Needs Analysis": 30,
    "Value Proposition": 40,
    "Negotiation": 60,
    "Closed Won": 100,
    "Closed Lost": 0,
}
QUOTE_STATUS = ["Draft", "Sent", "Accepted", "Rejected", "Expired"]
ORDER_STATUS = ["Draft", "Activated", "Cancelled"]


class SalesforceTestDataGenerator:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self.account_ids: List[str] = []
        self.account_names: Dict[str, str] = {}
        self.opportunity_ids: List[str] = []
        self.quote_ids: List[str] = []
        self.order_ids: List[str] = []

    def generate_id(self, prefix: str) -> str:
        return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    def generate_email(self, first_name: str, last_name: str, company_name: str) -> str:
        company_domain = company_name.lower().replace(" ", "").replace(".", "") + ".com"
        return f"{first_name.lower()}.{last_name.lower()}@{company_domain}"

    def generate_phone(self) -> str:
        return f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"

    def generate_accounts(self, count: int) -> List[Dict]:
        accounts = []
        for _ in range(count):
            account_id = self.generate_id("001")
            company_name = random.choice(COMPANY_NAMES) + f" {random.randint(1, 9999)}"
            self.account_ids.append(account_id)
            self.account_names[account_id] = company_name
            accounts.append({
                "Id": account_id,
                "Name": company_name,
                "BillingStreet": f"{random.randint(100, 9999)} Main Street",
                "BillingCity": random.choice(CITIES),
                "BillingState": random.choice(STATES),
                "BillingCountry": random.choice(COUNTRIES),
                "BillingPostalCode": f"{random.randint(10000, 99999)}",
                "Phone": self.generate_phone(),
                "Website": f"https://www.{company_name.lower().replace(' ', '').replace('.', '')}.com",
                "Industry": random.choice(INDUSTRIES),
                "AnnualRevenue": random.choice([500000, 1000000, 5000000, 10000000, 50000000, 100000000, 500000000]),
                "NumberOfEmployees": random.choice([10, 50, 100, 500, 1000, 5000, 10000]),
                "Description": f"Account created for testing. {random.choice(INDUSTRIES)} sector.",
            })
        return accounts

    def _distribute_total(self, parent_count: int, total_children: int, min_per_parent: int = 0) -> List[int]:
        if parent_count == 0:
            return []
        base = [min_per_parent] * parent_count
        remaining = max(0, total_children - sum(base))
        for _ in range(remaining):
            base[random.randint(0, parent_count - 1)] += 1
        return base

    def generate_contacts(self, contacts_per_account: Tuple[int, int] = (2, 4), total_contacts: Optional[int] = None) -> List[Dict]:
        contacts = []
        if total_contacts is not None:
            counts = self._distribute_total(len(self.account_ids), total_contacts)
        else:
            counts = [random.randint(*contacts_per_account) for _ in self.account_ids]

        for account_id, count in zip(self.account_ids, counts):
            for _ in range(count):
                first_name = random.choice(FIRST_NAMES)
                last_name = random.choice(LAST_NAMES)
                contacts.append({
                    "Id": self.generate_id("003"),
                    "FirstName": first_name,
                    "LastName": last_name,
                    "Email": self.generate_email(first_name, last_name, self.account_names[account_id]),
                    "Phone": self.generate_phone(),
                    "MobilePhone": self.generate_phone(),
                    "AccountId": account_id,
                    "Title": random.choice(TITLES),
                    "Department": random.choice(["Sales", "Engineering", "Marketing", "Finance", "Operations"]),
                    "MailingCity": random.choice(CITIES),
                    "MailingState": random.choice(STATES),
                    "MailingCountry": random.choice(COUNTRIES),
                    "Description": "Contact created for testing.",
                })
        return contacts

    def generate_opportunities(self, opps_per_account: Tuple[int, int] = (1, 3), total_opportunities: Optional[int] = None,
                               amount_min: int = 5000, amount_max: int = 500000,
                               stage_pool: Optional[Sequence[str]] = None) -> List[Dict]:
        opportunities = []
        stages = list(stage_pool) if stage_pool else OPPORTUNITY_STAGES
        if total_opportunities is not None:
            counts = self._distribute_total(len(self.account_ids), total_opportunities)
        else:
            counts = [random.randint(*opps_per_account) for _ in self.account_ids]

        stage_cycle = list(stages)
        random.shuffle(stage_cycle)
        idx = 0
        for account_id, count in zip(self.account_ids, counts):
            for j in range(count):
                opp_id = self.generate_id("006")
                self.opportunity_ids.append(opp_id)
                stage = stage_cycle[idx % len(stage_cycle)] if stage_cycle else random.choice(OPPORTUNITY_STAGES)
                idx += 1
                amount = random.randint(max(1, amount_min // 1000), max(1, amount_max // 1000)) * 1000
                opportunities.append({
                    "Id": opp_id,
                    "Name": f"{self.account_names[account_id]} - Opportunity {j + 1}",
                    "AccountId": account_id,
                    "StageName": stage,
                    "Amount": amount,
                    "Probability": STAGE_PROBABILITY.get(stage, 50),
                    "CloseDate": (datetime.now() + timedelta(days=random.randint(30, 180))).strftime("%Y-%m-%d"),
                    "Description": f"Test opportunity for account. Stage: {stage}",
                    "Type": random.choice(["New Business", "Existing Business", "Expansion"]),
                })
        return opportunities

    def generate_quotes(self, quote_ratio: float = 0.6) -> List[Dict]:
        selected_opps = random.sample(self.opportunity_ids, int(len(self.opportunity_ids) * quote_ratio)) if self.opportunity_ids else []
        quotes = []
        for i, opp_id in enumerate(selected_opps):
            quote_id = self.generate_id("701")
            self.quote_ids.append(quote_id)
            quotes.append({
                "Id": quote_id,
                "Name": f"Quote {i + 1}",
                "OpportunityId": opp_id,
                "QuoteNumber": f"Q-{random.randint(10000, 99999)}",
                "Status": random.choice(QUOTE_STATUS),
                "Total": random.randint(5, 500) * 1000,
                "ExpirationDate": (datetime.now() + timedelta(days=random.randint(14, 90))).strftime("%Y-%m-%d"),
                "Description": "Test quote created for testing",
            })
        return quotes

    def generate_orders(self, order_ratio: float = 0.7) -> List[Dict]:
        selected_quotes = random.sample(self.quote_ids, int(len(self.quote_ids) * order_ratio)) if self.quote_ids else []
        orders = []
        for quote_id in selected_quotes:
            order_id = self.generate_id("801")
            self.order_ids.append(order_id)
            orders.append({
                "Id": order_id,
                "QuoteId": quote_id,
                "OrderNumber": f"ORD-{random.randint(100000, 999999)}",
                "Status": random.choice(ORDER_STATUS),
                "EffectiveDate": datetime.now().strftime("%Y-%m-%d"),
                "TotalAmount": random.randint(5, 500) * 1000,
                "Description": "Test order created for testing",
            })
        return orders

    def generate_order_items(self, items_per_order: Tuple[int, int] = (2, 5)) -> List[Dict]:
        items = []
        for order_id in self.order_ids:
            for i in range(random.randint(*items_per_order)):
                items.append({
                    "OrderId": order_id,
                    "Description": f"Product/Service {i + 1}",
                    "Quantity": random.randint(1, 100),
                    "UnitPrice": random.choice([100, 500, 1000, 5000, 10000]),
                    "ListPrice": random.choice([100, 500, 1000, 5000, 10000]),
                    "ServiceDate": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
                })
        return items

    def generate_all(self, account_count: int = 50, include_contacts: bool = True, include_opportunities: bool = True,
                     include_quotes: bool = True, include_orders: bool = True, contacts_total: Optional[int] = None,
                     contacts_per_account: Tuple[int, int] = (2, 4), opps_total: Optional[int] = None,
                     opps_per_account: Tuple[int, int] = (1, 3), opp_amount_min: int = 5000, opp_amount_max: int = 500000,
                     opp_stages: Optional[Sequence[str]] = None) -> Dict:
        data: Dict[str, List[Dict]] = {}
        data["Accounts"] = self.generate_accounts(account_count)
        if include_contacts:
            data["Contacts"] = self.generate_contacts(contacts_per_account=contacts_per_account, total_contacts=contacts_total)
        if include_opportunities:
            data["Opportunities"] = self.generate_opportunities(
                opps_per_account=opps_per_account,
                total_opportunities=opps_total,
                amount_min=opp_amount_min,
                amount_max=opp_amount_max,
                stage_pool=opp_stages,
            )
        if include_quotes:
            data["Quotes"] = self.generate_quotes()
        if include_orders:
            data["Orders"] = self.generate_orders()
            data["OrderItems"] = self.generate_order_items()
        return data


def save_as_csv(data: Dict, output_dir: str = ".") -> None:
    import os
    os.makedirs(output_dir, exist_ok=True)
    for object_name, records in data.items():
        if records:
            with open(f"{output_dir}/{object_name}.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)


def save_as_json(data: Dict, output_file: str = "salesforce_test_data.json") -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def parse_range(value: str, default: Tuple[int, int]) -> Tuple[int, int]:
    if not value:
        return default
    left, right = value.split("-")
    return int(left), int(right)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Salesforce test data")
    parser.add_argument("--accounts", type=int, default=50)
    parser.add_argument("--contacts-total", type=int)
    parser.add_argument("--contacts-per-account", type=str, default="2-4")
    parser.add_argument("--opportunities-total", type=int)
    parser.add_argument("--opportunities-per-account", type=str, default="1-3")
    parser.add_argument("--opp-amount-min", type=int, default=5000)
    parser.add_argument("--opp-amount-max", type=int, default=500000)
    parser.add_argument("--opp-stages", type=str, help="Comma-separated stage list")
    parser.add_argument("--format", choices=["csv", "json", "both"], default="csv")
    parser.add_argument("--output", type=str, default=".")
    parser.add_argument("--no-contacts", action="store_true")
    parser.add_argument("--no-opportunities", action="store_true")
    parser.add_argument("--no-quotes", action="store_true")
    parser.add_argument("--no-orders", action="store_true")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    generator = SalesforceTestDataGenerator(seed=args.seed)
    data = generator.generate_all(
        account_count=args.accounts,
        include_contacts=not args.no_contacts,
        include_opportunities=not args.no_opportunities,
        include_quotes=not args.no_quotes,
        include_orders=not args.no_orders,
        contacts_total=args.contacts_total,
        contacts_per_account=parse_range(args.contacts_per_account, (2, 4)),
        opps_total=args.opportunities_total,
        opps_per_account=parse_range(args.opportunities_per_account, (1, 3)),
        opp_amount_min=args.opp_amount_min,
        opp_amount_max=args.opp_amount_max,
        opp_stages=[s.strip() for s in args.opp_stages.split(",")] if args.opp_stages else None,
    )

    if args.format in ["csv", "both"]:
        save_as_csv(data, args.output)
    if args.format in ["json", "both"]:
        save_as_json(data, args.output if args.format == "json" else f"{args.output}/salesforce_test_data.json")
