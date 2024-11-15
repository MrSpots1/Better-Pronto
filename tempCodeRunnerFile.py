print("\nDMs:")
    for dm in sorted_dms:
        print(f'{dm["title"]}; {dm["id"]}; Unread: {dm["unread"]}; '
              f'Unread Mentions: {dm["unread_mentions"]}; '
              f'Latest Message Created At: {dm["latest_message_created_at"]}')