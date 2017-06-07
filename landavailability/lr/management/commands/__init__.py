import time

def print_outcome_counts_and_rate(outcome_counts, start_time):
    total_count = sum(outcome_counts.values())
    rate_per_hour = total_count / (time.time() - start_time) * 60 * 60
    print(dict(outcome_counts), end=' ')
    print('Count: {:,} Rate: {:,.0f}/hour'
          .format(total_count, round(rate_per_hour, -3)))

def print_outcomes_and_rate(outcomes, start_time):
    total_count = sum([len(rows) for rows in outcomes.values()])
    rate_per_hour = total_count / (time.time() - start_time) * 60 * 60
    for outcome, rows in outcomes.items():
        print('{:,} {} e.g. {}'.format(len(rows), outcome, rows[0]))
    print('Count: {:,} Rate: {:,.0f}/hour'
          .format(total_count, round(rate_per_hour, -3)))
