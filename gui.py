import customtkinter as ctk
from engine import Game
from card_manager import CardManager

class App(ctk.CTk):
  def __init__(self):
    super().__init__(fg_color="#009600")
    self.geometry('1000x700+50+50')
    self.title('Blackjack')
    self.resizable(False, False)

    self.engine = Game()

    self.cards_manager = CardManager()

    self.result_string = ctk.StringVar(value='no result yet')

    self.current_bet_var = ctk.StringVar(value='')

    self.balance_var = ctk.StringVar(value=f'Balance: ₹{self.engine.get_current_balance()}')
    self.balance_label = ctk.CTkLabel(self, textvariable=self.balance_var, fg_color='black', width=105)
    self.balance_label.place(relx=0.01, rely=0.01, anchor='nw')

    self.deck_length = ctk.StringVar(value=f'Length of deck: {self.engine.get_deck_length()}')
    self.deck_length_label = ctk.CTkLabel(self, textvariable=self.deck_length, fg_color='black', width=120)
    self.deck_length_label.place(relx=0.99, rely=0.01, anchor='ne')

    self.dealer_hand_value_var = ctk.StringVar(value=f'Value: {self.engine.dealer_hand.value}')
    self.dealer_hand_value = ctk.CTkLabel(
      master=self,
      width=100,
      corner_radius=0,
      fg_color='black',
      text_color='white',
      textvariable=self.dealer_hand_value_var,
    )
    
    self.player_hand_value_var = ctk.StringVar(value=f'Value: {self.engine.player_hand.value}')
    self.player_hand_value = ctk.CTkLabel(
      master=self,
      width=100,
      corner_radius=0,
      fg_color='black',
      text_color='white',
      textvariable=self.player_hand_value_var,
    )
    
    self.dealer_card_holder = CardHolder(self, 0.5, 0.2)
    self.player_card_holder = CardHolder(self, 0.5, 0.8)
    self.middle_widget = MiddleWidget(
      parent=self,
      result_string=self.result_string,
      place_bet=self.place_bet,
      hit=self.hit,
      stand=self.stand,
      bet_var=self.current_bet_var,
      done=self.done
      )
    
    self.mainloop()

  def place_bet(self):
    try:
      bet = int(self.current_bet_var.get())
    except:
      self.current_bet_var.set('')
      self.middle_widget.bet_label.configure(text='Enter valid number!')
      return
    if self.engine.place_bet(bet):
      self.hide_bet()
      self.middle_widget.bet_label.configure(text='Enter the bet')
      self.engine.start_round()
      self.update_cards()
      self.update_extras()
      if self.engine.state == 'player_turn':
        self.show_hitstand()
      elif self.engine.state == 'round_over':
        self.show_result()
    else:
      self.current_bet_var.set('')
      self.middle_widget.bet_label.configure(text='Enter correct bet!')

  def update_cards(self):
    for widget in self.dealer_card_holder.winfo_children():
      widget.destroy()
    self.dealer_card_holder.configure(width=0, height=0)
    for widget in self.player_card_holder.winfo_children():
      widget.destroy()
    self.player_card_holder.configure(width=0, height=0)
    if self.engine.state == 'player_turn':
      for card in self.engine.get_player_cards():
        CardWidget(self.player_card_holder, self.cards_manager.card_images[(card.rank, card.suit)])
      CardWidget(self.dealer_card_holder, self.cards_manager.card_images[(self.engine.get_dealer_cards()[0].rank, self.engine.get_dealer_cards()[0].suit)])
      CardWidget(self.dealer_card_holder, self.cards_manager.special_images['back'])
      self.dealer_hand_value_var.set(f'Value: ??')
      self.player_hand_value_var.set(f'Value: {self.engine.player_hand.value}')
    elif self.engine.state == 'round_over':
      for card in self.engine.get_player_cards():
        CardWidget(self.player_card_holder, self.cards_manager.card_images[(card.rank, card.suit)])
      for card in self.engine.get_dealer_cards():
        CardWidget(self.dealer_card_holder, self.cards_manager.card_images[(card.rank, card.suit)])
      self.player_hand_value_var.set(f'Value: {self.engine.player_hand.value}')
      self.dealer_hand_value_var.set(f'Value: {self.engine.dealer_hand.value}')

    self.show_values()
    self.deck_length.set(f'Length of deck: {self.engine.get_deck_length()}')

  def hit(self):
    self.engine.player_hit()
    self.update_cards()
    if self.engine.state == 'round_over':
      self.hide_hitstand()
      self.show_result()
      self.update_extras()

  def stand(self):
    self.engine.player_stand()
    self.update_cards()
    self.hide_hitstand()
    self.show_result()
    self.update_extras()
  
  def update_extras(self):
    if self.engine.state == 'round_over':
      self.result_string.set(f'{self.engine.get_result()}')
    self.balance_var.set(f'Balance: ₹{self.engine.get_current_balance()}')

  def done(self):
    self.hide_result()
    self.show_bet()
    self.engine.reset_bankroll()
    self.update_extras()
    self.engine.reset_for_bet()
    self.update_cards()
    self.hide_values()

  def hide_values(self):
    self.dealer_hand_value.place_forget()
    self.player_hand_value.place_forget()

  def show_values(self):
    self.dealer_hand_value.place(relx=0.5, rely=0.35, anchor='center')
    self.player_hand_value.place(relx=0.5, rely=0.95, anchor='center')

  def hide_bet(self):
    self.middle_widget.bet_label.pack_forget()
    self.middle_widget.bet_entry.pack_forget()

  def show_bet(self):
    self.middle_widget.bet_label.pack(side='top', pady=10)
    self.middle_widget.bet_entry.pack(side='top')

  def show_hitstand(self):
    self.middle_widget.hitstand.pack(side='top', expand=True)

  def hide_hitstand(self):
    self.middle_widget.hitstand.pack_forget()

  def show_result(self):
    self.middle_widget.result.pack(side='top', expand=True)

  def hide_result(self):
    self.middle_widget.result.pack_forget()

class CardHolder(ctk.CTkFrame):
  def __init__(self, parent, relx, rely):
    super().__init__(
      master=parent,
      fg_color='transparent',
      width=0,
      height=0,
      corner_radius=0
      )
    self.place(relx=relx, rely=rely, anchor='center')

class CardWidget(ctk.CTkFrame):
  def __init__(self, parent, img):
    super().__init__(
      master=parent,
      width=84,
      height=120,
      fg_color='transparent',
      corner_radius=0)
    self.pack(side='left',padx=5, pady=5)
    self.pack_propagate(False)
    ctk.CTkLabel(
      master=self,
      image=img,
      text=''
    ).pack(expand=True)

class MiddleWidget(ctk.CTkFrame):
  def __init__(self, parent, result_string, place_bet, hit, stand, bet_var, done):
    super().__init__(
      master=parent,
      fg_color='transparent',
      border_color='black',
      border_width=1,
      corner_radius=0
    )
    self.place(relx=0.5, rely=0.5, relwidth=1, relheight=0.2, anchor='center')

    self.bet_label = ctk.CTkLabel(
      master=self,
      fg_color='transparent',
      text='Enter the bet',
      text_color='black',
      corner_radius=0,
      width=150,
      font=('idk-Default', 20, 'bold')
    )
    self.bet_label.pack(side='top', pady=10)

    self.bet_entry = ctk.CTkEntry(
      master=self,
      fg_color='#eeeeee',
      text_color='black',
      corner_radius=0,
      textvariable=bet_var
    )
    self.bet_entry.pack(side='top')
    self.bet_entry.bind('<Return>', lambda event: place_bet())

    self.hitstand = HitStand(self, hit, stand)

    self.result = Result(parent=self, done=done, result_string=result_string)

class Result(ctk.CTkFrame):
  def __init__(self, parent, done, result_string):
    super().__init__(
      master=parent,
      fg_color='transparent',
      width=0,
      height=0
    )

    self.result_label = ctk.CTkLabel(
      master=self,
      textvariable=result_string,
      fg_color='black',
      corner_radius=0,
      width=180,
      font=('idk-Default', 20, 'bold')
    )
    self.result_label.pack(side='top', pady=10)

    self.done_button = ctk.CTkButton(
      master=self,
      text='Done',
      text_color='white',
      fg_color="#00BE00",
      corner_radius=0,
      hover_color="#00a500",
      command=done
    )
    self.done_button.pack(side='top')

class HitStand(ctk.CTkFrame):
  def __init__(self, parent, hit, stand):
    super().__init__(
      master=parent,
      fg_color='transparent',
      width=0,
      height=0
    )

    self.hit = ctk.CTkButton(
      master=self,
      text='Hit',
      text_color='white',
      fg_color="#c50000",
      corner_radius=0,
      hover_color="#a00000",
      command=hit
    )
    self.hit.pack(side='left', expand=True, padx=10)

    self.stand = ctk.CTkButton(
      master=self,
      text='Stand',
      text_color='white',
      fg_color="#1561d3",
      corner_radius=0,
      hover_color="#016c9d",
      command=stand
    )
    self.stand.pack(side='left', expand=True, padx=10)

App()