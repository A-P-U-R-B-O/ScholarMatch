"""
ScholarMatch - Database Operations Module
Handles loading and saving scholarship and user data
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random


def load_scholarships(filepath: str = "data/scholarships.json") -> List[Dict[str, Any]]:
    """
    Load scholarships from JSON file
    If file doesn't exist, create sample data
    
    Args:
        filepath: Path to scholarships JSON file
    
    Returns:
        List of scholarship dictionaries
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                scholarships = json.load(f)
                print(f"✅ Loaded {len(scholarships)} scholarships from {filepath}")
                return scholarships
        else:
            print(f"⚠️ File {filepath} not found. Creating sample data...")
            scholarships = generate_sample_scholarships()
            save_scholarships(scholarships, filepath)
            return scholarships
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")
        print("Creating sample data instead...")
        scholarships = generate_sample_scholarships()
        save_scholarships(scholarships, filepath)
        return scholarships
    except Exception as e:
        print(f"❌ Error loading scholarships: {e}")
        return []


def save_scholarships(scholarships: List[Dict[str, Any]], filepath: str = "data/scholarships.json") -> bool:
    """
    Save scholarships to JSON file
    
    Args:
        scholarships: List of scholarship dictionaries
        filepath: Path to save JSON file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scholarships, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(scholarships)} scholarships to {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error saving scholarships: {e}")
        return False


def load_users(filepath: str = "data/users.json") -> List[Dict[str, Any]]:
    """
    Load user profiles from JSON file
    
    Args:
        filepath: Path to users JSON file
    
    Returns:
        List of user profile dictionaries
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                users = json.load(f)
                print(f"✅ Loaded {len(users)} user profiles")
                return users
        else:
            print(f"ℹ️ No existing users file. Creating new one...")
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []
    except Exception as e:
        print(f"❌ Error loading users: {e}")
        return []


def save_user_profile(profile: Dict[str, Any], filepath: str = "data/users.json") -> bool:
    """
    Save user profile to JSON file (appends to existing profiles)
    
    Args:
        profile: User profile dictionary
        filepath: Path to users JSON file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load existing profiles
        users = load_users(filepath)
        
        # Add timestamp
        profile['created_at'] = datetime.utcnow().isoformat()
        profile['id'] = len(users) + 1
        
        # Append new profile
        users.append(profile)
        
        # Save back to file
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved user profile for {profile.get('name', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Error saving user profile: {e}")
        return False


def get_user_by_email(email: str, filepath: str = "data/users.json") -> Dict[str, Any]:
    """
    Retrieve user profile by email
    
    Args:
        email: User's email address
        filepath: Path to users JSON file
    
    Returns:
        User profile dictionary or None if not found
    """
    users = load_users(filepath)
    for user in users:
        if user.get('email', '').lower() == email.lower():
            return user
    return None


def calculate_deadline_days(deadline_str: str) -> int:
    """
    Calculate days until deadline from date string
    
    Args:
        deadline_str: Date string in YYYY-MM-DD format
    
    Returns:
        Number of days until deadline
    """
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        today = datetime.utcnow()
        delta = deadline - today
        return max(0, delta.days)  # Return 0 if deadline has passed
    except Exception as e:
        print(f"⚠️ Error calculating deadline: {e}")
        return 999  # Return large number if error


def update_scholarship_deadlines(scholarships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Update deadline_days field for all scholarships based on current date
    
    Args:
        scholarships: List of scholarship dictionaries
    
    Returns:
        Updated list of scholarships
    """
    for scholarship in scholarships:
        if 'deadline' in scholarship:
            scholarship['deadline_days'] = calculate_deadline_days(scholarship['deadline'])
    return scholarships


def search_scholarships(scholarships: List[Dict[str, Any]], 
                       query: str = "",
                       category: str = None,
                       min_amount: int = None,
                       max_amount: int = None) -> List[Dict[str, Any]]:
    """
    Search scholarships by keyword, category, or amount
    
    Args:
        scholarships: List of scholarship dictionaries
        query: Search keyword (searches name and description)
        category: Filter by category
        min_amount: Minimum scholarship amount
        max_amount: Maximum scholarship amount
    
    Returns:
        Filtered list of scholarships
    """
    results = scholarships.copy()
    
    # Filter by keyword
    if query:
        query_lower = query.lower()
        results = [
            s for s in results 
            if query_lower in s.get('name', '').lower() 
            or query_lower in s.get('description', '').lower()
            or query_lower in s.get('category', '').lower()
        ]
    
    # Filter by category
    if category:
        results = [s for s in results if s.get('category', '') == category]
    
    # Filter by amount
    if min_amount is not None:
        results = [
            s for s in results 
            if isinstance(s.get('amount'), (int, float)) and s.get('amount', 0) >= min_amount
        ]
    
    if max_amount is not None:
        results = [
            s for s in results 
            if isinstance(s.get('amount'), (int, float)) and s.get('amount', 0) <= max_amount
        ]
    
    return results


def get_categories(scholarships: List[Dict[str, Any]]) -> List[str]:
    """
    Get unique categories from scholarships
    
    Args:
        scholarships: List of scholarship dictionaries
    
    Returns:
        Sorted list of unique categories
    """
    categories = set()
    for scholarship in scholarships:
        cat = scholarship.get('category', 'General')
        categories.add(cat)
    return sorted(list(categories))


def get_scholarship_by_name(name: str, scholarships: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Find scholarship by exact name match
    
    Args:
        name: Scholarship name
        scholarships: List of scholarship dictionaries
    
    Returns:
        Scholarship dictionary or None if not found
    """
    for scholarship in scholarships:
        if scholarship.get('name', '').lower() == name.lower():
            return scholarship
    return None


def generate_sample_scholarships() -> List[Dict[str, Any]]:
    """
    Generate sample scholarship data for demo purposes
    This is a fallback if the JSON file doesn't exist
    
    Returns:
        List of sample scholarship dictionaries
    """
    # Calculate dates relative to current date (2025-11-04)
    base_date = datetime(2025, 11, 4)
    
    sample_scholarships = [
        {
            "name": "STEM Excellence Scholarship",
            "amount": 5000,
            "deadline": (base_date + timedelta(days=45)).strftime("%Y-%m-%d"),
            "deadline_days": 45,
            "min_gpa": 3.5,
            "majors": ["STEM", "Engineering"],
            "grade_levels": ["High School Senior", "College Freshman"],
            "states": ["All"],
            "demographics": [],
            "interests": ["STEM Clubs"],
            "special_circumstances": [],
            "category": "STEM",
            "description": "Annual scholarship for students pursuing STEM degrees with demonstrated academic excellence.",
            "requirements": ["Essay (500 words)", "2 Recommendation Letters", "Transcript"],
            "url": "https://example.com/stem-scholarship",
            "eligibility": "Minimum 3.5 GPA, pursuing STEM degree"
        },
        {
            "name": "First Generation Scholar Award",
            "amount": 10000,
            "deadline": (base_date + timedelta(days=26)).strftime("%Y-%m-%d"),
            "deadline_days": 26,
            "min_gpa": 3.0,
            "majors": ["Any"],
            "grade_levels": ["High School Senior"],
            "states": ["All"],
            "demographics": [],
            "interests": [],
            "special_circumstances": ["First Generation College Student"],
            "category": "First Generation",
            "description": "Supporting first-generation college students in their educational journey.",
            "requirements": ["Personal Statement", "Proof of first-gen status", "Transcript"],
            "url": "https://example.com/first-gen",
            "eligibility": "First generation college student, minimum 3.0 GPA"
        },
        {
            "name": "Women in Technology Grant",
            "amount": 7500,
            "deadline": (base_date + timedelta(days=88)).strftime("%Y-%m-%d"),
            "deadline_days": 88,
            "min_gpa": 3.2,
            "majors": ["STEM", "Engineering"],
            "grade_levels": ["College Sophomore", "College Junior", "College Senior"],
            "states": ["All"],
            "demographics": ["Female"],
            "interests": ["STEM Clubs", "Entrepreneurship"],
            "special_circumstances": [],
            "category": "Women in STEM",
            "description": "Empowering women pursuing technology and engineering careers.",
            "requirements": ["Project Portfolio", "Essay", "Recommendation"],
            "url": "https://example.com/women-tech",
            "eligibility": "Female students in STEM fields, min 3.2 GPA"
        }
    ]
    
    return sample_scholarships


def export_matches_to_json(matches: List[Dict[str, Any]], filename: str = "my_matches.json") -> str:
    """
    Export matched scholarships to a JSON file for download
    
    Args:
        matches: List of matched scholarship dictionaries
        filename: Output filename
    
    Returns:
        Filepath of exported file
    """
    try:
        output_path = f"exports/{filename}"
        os.makedirs("exports", exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(matches)} matches to {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error exporting matches: {e}")
        return ""


def get_statistics(scholarships: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate overall statistics from scholarship database
    
    Args:
        scholarships: List of scholarship dictionaries
    
    Returns:
        Dictionary of statistics
    """
    if not scholarships:
        return {
            "total_scholarships": 0,
            "total_funding": 0,
            "avg_amount": 0,
            "categories": {},
            "urgent_deadlines": 0
        }
    
    # Calculate totals
    amounts = [s.get('amount', 0) for s in scholarships if isinstance(s.get('amount'), (int, float))]
    total_funding = sum(amounts)
    avg_amount = int(total_funding / len(amounts)) if amounts else 0
    
    # Category breakdown
    categories = {}
    for s in scholarships:
        cat = s.get('category', 'General')
        categories[cat] = categories.get(cat, 0) + 1
    
    # Count urgent deadlines (< 30 days)
    urgent = len([s for s in scholarships if s.get('deadline_days', 999) < 30])
    
    return {
        "total_scholarships": len(scholarships),
        "total_funding": total_funding,
        "avg_amount": avg_amount,
        "categories": categories,
        "urgent_deadlines": urgent
    }


def validate_scholarship_data(scholarship: Dict[str, Any]) -> tuple:
    """
    Validate scholarship data structure
    
    Args:
        scholarship: Scholarship dictionary
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    required_fields = ['name', 'amount', 'deadline', 'category']
    
    for field in required_fields:
        if field not in scholarship:
            errors.append(f"Missing required field: {field}")
    
    # Validate amount
    if 'amount' in scholarship:
        if not isinstance(scholarship['amount'], (int, float)) or scholarship['amount'] <= 0:
            errors.append("Amount must be a positive number")
    
    # Validate deadline format
    if 'deadline' in scholarship:
        try:
            datetime.strptime(scholarship['deadline'], "%Y-%m-%d")
        except ValueError:
            errors.append("Deadline must be in YYYY-MM-DD format")
    
    # Validate GPA
    if 'min_gpa' in scholarship:
        if not isinstance(scholarship['min_gpa'], (int, float)) or not (0 <= scholarship['min_gpa'] <= 4.0):
            errors.append("GPA must be between 0 and 4.0")
    
    return (len(errors) == 0, errors)


# Test functions
if __name__ == "__main__":
    print("🧪 Testing database.py functions...\n")
    
    # Test 1: Load scholarships
    print("Test 1: Loading scholarships...")
    scholarships = load_scholarships()
    print(f"Loaded {len(scholarships)} scholarships\n")
    
    # Test 2: Get categories
    print("Test 2: Getting categories...")
    categories = get_categories(scholarships)
    print(f"Found {len(categories)} categories: {categories[:5]}...\n")
    
    # Test 3: Search scholarships
    print("Test 3: Searching for 'STEM' scholarships...")
    stem_scholarships = search_scholarships(scholarships, query="STEM")
    print(f"Found {len(stem_scholarships)} STEM scholarships\n")
    
    # Test 4: Get statistics
    print("Test 4: Getting statistics...")
    stats = get_statistics(scholarships)
    print(f"Total funding available: ${stats['total_funding']:,}")
    print(f"Average scholarship amount: ${stats['avg_amount']:,}")
    print(f"Urgent deadlines: {stats['urgent_deadlines']}\n")
    
    # Test 5: Save sample user
    print("Test 5: Saving sample user profile...")
    sample_user = {
        "name": "Test Student",
        "email": "test@example.com",
        "gpa": 3.5,
        "major": "STEM",
        "grade_level": "High School Senior",
        "state": "California"
    }
    save_user_profile(sample_user)
    
    # Test 6: Load user by email
    print("Test 6: Loading user by email...")
    user = get_user_by_email("test@example.com")
    if user:
        print(f"Found user: {user['name']}\n")
    
    print("✅ All tests completed!")
