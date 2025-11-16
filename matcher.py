"""
ScholarMatch - Scholarship Matching Algorithm
Matches user profiles to scholarships using weighted scoring system with Hard Filters
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Tuple


def calculate_match_score(user_profile: Dict[str, Any], scholarship: Dict[str, Any]) -> Tuple[int, List[str]]:
    """
    Calculate match score between user profile and scholarship with Hard Filters
    
    HARD FILTERS (must pass or immediate 0% match):
    1. GPA - Must meet minimum requirement
    2. Grade Level - Must be in allowed list
    3. State/Location - Must match if not 'All'
    
    Args:
        user_profile: Dictionary containing user information
        scholarship: Dictionary containing scholarship information
    
    Returns:
        Tuple of (match_score, match_reasons)
    """
    
    # ==================== HARD FILTERS ====================
    # These must ALL pass or scholarship gets 0% match immediately
    
    # HARD FILTER 1: GPA Check
    min_gpa = scholarship.get('min_gpa', 0.0)
    user_gpa = user_profile.get('gpa', 0.0)
    
    if min_gpa > 0 and user_gpa < min_gpa:
        return (0, [f"❌ HARD FAIL: GPA requirement not met (need {min_gpa}, have {user_gpa})"])
    
    # HARD FILTER 2: Grade Level Check
    required_grades = scholarship.get('grade_levels', [])
    user_grade = user_profile.get('grade_level', '')
    
    if required_grades and user_grade not in required_grades:
        return (0, [f"❌ HARD FAIL: Grade level not eligible (need: {', '.join(required_grades)}, have: {user_grade})"])
    
    # HARD FILTER 3: State/Location Check (only if not 'All')
    required_states = scholarship.get('states', [])
    user_state = user_profile.get('state', '')
    
    if required_states and 'All' not in required_states and user_state not in required_states:
        return (0, [f"❌ HARD FAIL: Location not eligible (need: {', '.join(required_states)}, have: {user_state})"])
    
    # ==================== PASSED HARD FILTERS ====================
    # Now proceed with weighted scoring
    
    score = 0
    max_score = 0
    reasons = []
    
    # 1. GPA Match (Weight: 20 points)
    max_score += 20
    if user_gpa >= min_gpa:
        score += 20
        if min_gpa > 0:
            reasons.append(f"✓ Meets GPA requirement ({min_gpa})")
        else:
            reasons.append(f"✓ No GPA requirement")
    
    # 2. Major Match (Weight: 25 points)
    max_score += 25
    required_majors = scholarship.get('majors', [])
    user_major = user_profile.get('major', '')
    
    if not required_majors or 'Any' in required_majors or user_major in required_majors:
        score += 25
        if required_majors and user_major in required_majors:
            reasons.append(f"✓ Perfect major match: {user_major}")
        elif not required_majors or 'Any' in required_majors:
            reasons.append("✓ Open to all majors")
    else:
        reasons.append(f"○ Major preference: {', '.join(required_majors)} (you have: {user_major})")
    
    # 3. Grade Level Match (Weight: 20 points)
    max_score += 20
    if not required_grades or user_grade in required_grades:
        score += 20
        reasons.append(f"✓ Grade level eligible")
    
    # 4. State/Location Match (Weight: 10 points)
    max_score += 10
    if not required_states or 'All' in required_states or user_state in required_states:
        score += 10
        if required_states and user_state in required_states and 'All' not in required_states:
            reasons.append(f"✓ State match: {user_state}")
        else:
            reasons.append(f"✓ Available nationwide")
    
    # 5. Demographics Match (Weight: 10 points)
    max_score += 10
    required_demographics = scholarship.get('demographics', [])
    user_ethnicity = user_profile.get('ethnicity', [])
    user_gender = user_profile.get('gender', '')
    
    if not required_demographics:
        score += 5  # Open to all
        reasons.append("✓ No demographic restrictions")
    else:
        demographic_match = False
        
        # Check ethnicity match
        if any(eth in required_demographics for eth in user_ethnicity):
            score += 5
            demographic_match = True
            matching_eth = [eth for eth in user_ethnicity if eth in required_demographics]
            reasons.append(f"✓ Demographics match: {', '.join(matching_eth)}")
        
        # Check gender match
        if user_gender in required_demographics and user_gender != 'Prefer not to say':
            score += 5
            demographic_match = True
            reasons.append(f"✓ Gender match: {user_gender}")
        
        if not demographic_match and required_demographics:
            reasons.append(f"○ Demographic preference: {', '.join(required_demographics[:2])}")
    
    # 6. Interests Match (Weight: 10 points)
    max_score += 10
    required_interests = scholarship.get('interests', [])
    user_interests = user_profile.get('interests', [])
    
    if required_interests:
        matching_interests = set(user_interests) & set(required_interests)
        if matching_interests:
            # Award points based on number of matching interests
            interest_score = min(10, len(matching_interests) * 3)
            score += interest_score
            reasons.append(f"✓ Interests: {', '.join(list(matching_interests)[:3])}")
        else:
            reasons.append(f"○ Preferred interests: {', '.join(required_interests[:2])}")
    else:
        score += 5  # No specific interests required
        reasons.append("✓ No interest requirements")
    
    # 7. Special Circumstances Match (Weight: 5 points)
    max_score += 5
    required_circumstances = scholarship.get('special_circumstances', [])
    user_circumstances = user_profile.get('special_circumstances', [])
    
    if required_circumstances:
        matching_circumstances = set(user_circumstances) & set(required_circumstances)
        if matching_circumstances:
            score += 5
            reasons.append(f"✓ Special: {', '.join(matching_circumstances)}")
        else:
            reasons.append(f"○ Preference for: {', '.join(required_circumstances)}")
    else:
        score += 2  # No specific circumstances required
    
    # Calculate final percentage
    match_percentage = int((score / max_score) * 100) if max_score > 0 else 0
    
    return match_percentage, reasons


def match_scholarships(user_profile: Dict[str, Any], scholarships: List[Dict[str, Any]], 
                       min_match_threshold: int = 40) -> List[Dict[str, Any]]:
    """
    Match scholarships to user profile and return sorted results
    
    Args:
        user_profile: User profile dictionary
        scholarships: List of scholarship dictionaries
        min_match_threshold: Minimum match percentage to include (default: 40%)
    
    Returns:
        List of matched scholarships with scores, sorted by match percentage
    """
    matches = []
    hard_failures = []
    
    for scholarship in scholarships:
        match_score, match_reasons = calculate_match_score(user_profile, scholarship)
        
        # Track hard failures separately for analytics
        if match_score == 0 and any('HARD FAIL' in reason for reason in match_reasons):
            hard_failures.append({
                'name': scholarship['name'],
                'reason': match_reasons[0]
            })
            continue
        
        # Only include scholarships above threshold
        if match_score >= min_match_threshold:
            scholarship_copy = scholarship.copy()
            scholarship_copy['match_score'] = match_score
            scholarship_copy['match_reasons'] = match_reasons
            
            # Add urgency level based on deadline
            deadline_days = scholarship.get('deadline_days', 999)
            if deadline_days < 7:
                scholarship_copy['urgency'] = 'critical'
            elif deadline_days < 30:
                scholarship_copy['urgency'] = 'high'
            elif deadline_days < 90:
                scholarship_copy['urgency'] = 'medium'
            else:
                scholarship_copy['urgency'] = 'low'
            
            matches.append(scholarship_copy)
    
    # Sort by match score (descending), then by amount (descending), then by deadline (ascending)
    matches.sort(key=lambda x: (
        -x['match_score'],  # Higher match score first
        -x.get('amount', 0) if isinstance(x.get('amount'), (int, float)) else 0,  # Higher amount first
        x.get('deadline_days', 999)  # Closer deadline first
    ))
    
    # Optional: Log hard failures for debugging
    if hard_failures:
        print(f"📊 Hard Filter Stats: {len(hard_failures)} scholarships excluded due to hard requirements")
        for failure in hard_failures[:5]:  # Show first 5
            print(f"   • {failure['name']}: {failure['reason']}")
    
    return matches


def get_scholarship_statistics(matches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate statistics from matched scholarships
    
    Args:
        matches: List of matched scholarship dictionaries
    
    Returns:
        Dictionary containing statistics
    """
    if not matches:
        return {
            'total_matches': 0,
            'total_potential_value': 0,
            'average_match_score': 0,
            'urgent_deadlines': 0,
            'categories': {}
        }
    
    # Calculate total potential value
    amounts = [s.get('amount', 0) for s in matches if isinstance(s.get('amount'), (int, float))]
    total_value = sum(amounts[:10])  # Top 10 scholarships
    
    # Calculate average match score
    avg_score = sum([s.get('match_score', 0) for s in matches]) / len(matches)
    
    # Count urgent deadlines
    urgent = len([s for s in matches if s.get('deadline_days', 999) < 30])
    
    # Category breakdown
    categories = {}
    for s in matches:
        cat = s.get('category', 'General')
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        'total_matches': len(matches),
        'total_potential_value': total_value,
        'average_match_score': int(avg_score),
        'urgent_deadlines': urgent,
        'categories': categories
    }


def filter_scholarships(matches: List[Dict[str, Any]], 
                       category: str = None,
                       min_amount: int = None,
                       max_amount: int = None,
                       deadline_range: str = None) -> List[Dict[str, Any]]:
    """
    Filter matched scholarships based on criteria
    
    Args:
        matches: List of matched scholarships
        category: Filter by category
        min_amount: Minimum scholarship amount
        max_amount: Maximum scholarship amount
        deadline_range: 'week', 'month', 'quarter', 'year'
    
    Returns:
        Filtered list of scholarships
    """
    filtered = matches.copy()
    
    # Filter by category
    if category:
        filtered = [s for s in filtered if s.get('category', '') == category]
    
    # Filter by amount
    if min_amount is not None:
        filtered = [s for s in filtered if isinstance(s.get('amount'), (int, float)) and s.get('amount', 0) >= min_amount]
    
    if max_amount is not None:
        filtered = [s for s in filtered if isinstance(s.get('amount'), (int, float)) and s.get('amount', 0) <= max_amount]
    
    # Filter by deadline
    if deadline_range:
        deadline_limits = {
            'week': 7,
            'month': 30,
            'quarter': 90,
            'year': 365
        }
        max_days = deadline_limits.get(deadline_range, 365)
        filtered = [s for s in filtered if s.get('deadline_days', 999) <= max_days]
    
    return filtered


def get_hard_filter_failures(user_profile: Dict[str, Any], scholarships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get list of scholarships that failed hard filters with reasons
    Useful for analytics and understanding why students don't match certain scholarships
    
    Args:
        user_profile: User profile dictionary
        scholarships: List of scholarship dictionaries
    
    Returns:
        List of dictionaries with scholarship name and failure reason
    """
    failures = []
    
    for scholarship in scholarships:
        match_score, match_reasons = calculate_match_score(user_profile, scholarship)
        
        if match_score == 0 and any('HARD FAIL' in reason for reason in match_reasons):
            failures.append({
                'scholarship': scholarship['name'],
                'amount': scholarship.get('amount', 'Varies'),
                'category': scholarship.get('category', 'General'),
                'failure_reason': match_reasons[0]
            })
    
    return failures


if __name__ == "__main__":
    # Test the matching algorithm with hard filters
    print("🧪 Testing Hard Filter Logic...\n")
    
    # Test Case 1: Student who passes all hard filters
    test_user_pass = {
        'name': 'Test Student (PASS)',
        'gpa': 3.7,
        'major': 'STEM',
        'grade_level': 'High School Senior',
        'state': 'California',
        'ethnicity': ['Asian American'],
        'gender': 'Female',
        'interests': ['STEM Clubs', 'Community Service'],
        'special_circumstances': ['First Generation College Student']
    }
    
    test_scholarship = {
        'name': 'Test STEM Scholarship',
        'amount': 5000,
        'min_gpa': 3.5,
        'majors': ['STEM'],
        'grade_levels': ['High School Senior'],
        'states': ['California', 'New York'],
        'demographics': ['Female'],
        'interests': ['STEM Clubs'],
        'special_circumstances': ['First Generation College Student'],
        'deadline_days': 30,
        'category': 'STEM'
    }
    
    score, reasons = calculate_match_score(test_user_pass, test_scholarship)
    print("=" * 60)
    print("TEST 1: Student PASSES all hard filters")
    print("=" * 60)
    print(f"Match Score: {score}%")
    print("Reasons:")
    for reason in reasons:
        print(f"  {reason}")
    print()
    
    # Test Case 2: Student fails GPA hard filter
    test_user_fail_gpa = {
        'name': 'Test Student (FAIL GPA)',
        'gpa': 3.2,  # Below minimum
        'major': 'STEM',
        'grade_level': 'High School Senior',
        'state': 'California',
        'ethnicity': ['Asian American'],
        'gender': 'Female',
        'interests': ['STEM Clubs'],
        'special_circumstances': []
    }
    
    score, reasons = calculate_match_score(test_user_fail_gpa, test_scholarship)
    print("=" * 60)
    print("TEST 2: Student FAILS GPA hard filter")
    print("=" * 60)
    print(f"Match Score: {score}%")
    print("Reasons:")
    for reason in reasons:
        print(f"  {reason}")
    print()
    
    # Test Case 3: Student fails Grade Level hard filter
    test_user_fail_grade = {
        'name': 'Test Student (FAIL GRADE)',
        'gpa': 3.8,
        'major': 'STEM',
        'grade_level': 'College Sophomore',  # Not in allowed list
        'state': 'California',
        'ethnicity': ['Asian American'],
        'gender': 'Female',
        'interests': ['STEM Clubs'],
        'special_circumstances': []
    }
    
    score, reasons = calculate_match_score(test_user_fail_grade, test_scholarship)
    print("=" * 60)
    print("TEST 3: Student FAILS Grade Level hard filter")
    print("=" * 60)
    print(f"Match Score: {score}%")
    print("Reasons:")
    for reason in reasons:
        print(f"  {reason}")
    print()
    
    # Test Case 4: Student fails State hard filter
    test_user_fail_state = {
        'name': 'Test Student (FAIL STATE)',
        'gpa': 3.8,
        'major': 'STEM',
        'grade_level': 'High School Senior',
        'state': 'Texas',  # Not in allowed states
        'ethnicity': ['Asian American'],
        'gender': 'Female',
        'interests': ['STEM Clubs'],
        'special_circumstances': []
    }
    
    score, reasons = calculate_match_score(test_user_fail_state, test_scholarship)
    print("=" * 60)
    print("TEST 4: Student FAILS State hard filter")
    print("=" * 60)
    print(f"Match Score: {score}%")
    print("Reasons:")
    for reason in reasons:
        print(f"  {reason}")
    print()
    
    # Test Case 5: Scholarship with 'All' states (should pass)
    test_scholarship_all_states = test_scholarship.copy()
    test_scholarship_all_states['states'] = ['All']
    test_scholarship_all_states['name'] = 'National Scholarship (All States)'
    
    score, reasons = calculate_match_score(test_user_fail_state, test_scholarship_all_states)
    print("=" * 60)
    print("TEST 5: Scholarship with 'All' states (should PASS)")
    print("=" * 60)
    print(f"Match Score: {score}%")
    print("Reasons:")
    for reason in reasons:
        print(f"  {reason}")
    print()
    
    print("✅ All hard filter tests completed!")
