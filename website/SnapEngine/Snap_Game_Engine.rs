use std::collections::HashMap;

#[derive(Debug)]
struct Event {
    name: String,
    odds: HashMap<String, f64>,
}

#[derive(Debug)]
struct Bet {
    event: String,
    outcome: String,
    amount: f64,
}

struct Sportsbook {
    events: HashMap<String, Event>,
    bets: Vec<Bet>,
}

impl Sportsbook {
    fn new() -> Self {
        Sportsbook {
            events: HashMap::new(),
            bets: Vec::new(),
        }
    }

    fn add_event(&mut self, name: &str, odds: HashMap<String, f64>) {
        self.events.insert(
            name.to_string(),
            Event {
                name: name.to_string(),
                odds,
            },
        );
    }

    fn place_bet(&mut self, event: &str, outcome: &str, amount: f64) -> Result<(), String> {
        if let Some(event_data) = self.events.get(event) {
            if event_data.odds.contains_key(outcome) {
                self.bets.push(Bet {
                    event: event.to_string(),
                    outcome: outcome.to_string(),
                    amount,
                });
                Ok(())
            } else {
                Err(format!("Invalid outcome for event: {}", event))
            }
        } else {
            Err(format!("Event not found: {}", event))
        }
    }

    fn calculate_payout(&self, bet: &Bet) -> Option<f64> {
        if let Some(event) = self.events.get(&bet.event) {
            if let Some(odds) = event.odds.get(&bet.outcome) {
                Some(bet.amount * odds)
            } else {
                None
            }
        } else {
            None
        }
    }

    fn settle_event(&mut self, event: &str, outcome: &str) -> Vec<f64> {
        let mut payouts = Vec::new();
        self.bets.retain(|bet| {
            if bet.event == event {
                if bet.outcome == outcome {
                    if let Some(payout) = self.calculate_payout(bet) {
                        payouts.push(payout);
                    }
                }
                false // Remove the bet
            } else {
                true // Keep the bet
            }
        });
        payouts
    }
}

fn main() {
    let mut sportsbook = Sportsbook::new();

    // Add an event
    let mut odds = HashMap::new();
    odds.insert("Team A".to_string(), 2.0);
    odds.insert("Team B".to_string(), 1.8);
    odds.insert("Draw".to_string(), 3.5);
    sportsbook.add_event("Football Match", odds);

    // Place some bets
    sportsbook.place_bet("Football Match", "Team A", 100.0).unwrap();
    sportsbook.place_bet("Football Match", "Team B", 150.0).unwrap();
    sportsbook.place_bet("Football Match", "Draw", 50.0).unwrap();

    // Settle the event
    let payouts = sportsbook.settle_event("Football Match", "Team A");

    println!("Payouts: {:?}", payouts);
}