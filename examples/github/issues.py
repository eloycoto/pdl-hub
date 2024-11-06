import requests


def fetch_open_issues(owner, repo, sort_by='created', direction='desc'):
    """
    Fetch open issues from a GitHub repository.

    Parameters:
    owner (str): Repository owner/organization name
    repo (str): Repository name
    sort_by (str): Sort issues by 'created', 'updated', or 'comments'
    direction (str): Sort direction, 'asc' or 'desc'
    Returns:
    list: List of open issues with their details
    """
    base_url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    params = {
        'state': 'open',
        'sort': sort_by,
        'direction': direction,
        'per_page': 100  # Maximum issues per page
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(base_url, params=params, headers=headers)
    response.raise_for_status()
    issues = response.json()

    formatted_issues = []
    for issue in issues:
        if 'pull_request' in issue:
            continue
        formatted_issue = {
            'number': issue['number'],
            'title': issue['title'],
            'state': issue['state'],
            'created_at': issue['created_at'],
            'body': issue['body'],
            'author': issue['user']['login'],
            'labels': [label['name'] for label in issue['labels']],
            'comments': issue['comments'],
            'url': issue['html_url']
        }
        formatted_issues.append(formatted_issue)
    return formatted_issues
