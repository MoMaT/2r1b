## 2r1b

Character card generator for ["Two room and a boom"][2r1b] game.
Intended to replace the [original print & play][PnP] version which is
quite ugly and does not contain useful description of the roles.

Released to Public Domain (under the terms of the [CC0 licence][CC0]).

I have changed names of some characters, either to shorten it and fit on
the card better, or to make more sense:

* Tuesday Knight -> Hero
* Psychologist -> Therapist

You can edit the descriptions of the roles in `data/cards.json`.

The setup of a page is 2x4 cards on A4 page in landscape orientation.
Each card is 59mm width and 92mm height.

To set cards on a page, change lines like this in `build.py`:

```python
roles = "President, Bomber, Doctor, Engineer, Nurse, Tinkerer, President's daughter, Martyr"
pages.append([cards[name] for name in roles.split(", ")])
```

Some characters have cards in both colours and take 2 slots on a page:

```python
roles = "Negotiator, Coy boy, Angel, Demon"
pages.append([cards[name] for name in roles.split(", ")])
```

Check [how the cards look][cards] when printed and put in black back sleeves.


[2r1b]: http://tuesdayknightgames.com/tworoomsandaboom/
[PnP]: http://tuesdayknightgames.com/downloads/2R1B%20Playset%20with%20Leaders_v4.zip
[CC0]: http://creativecommons.org/publicdomain/zero/1.0/
[cards]: https://github.com/MoMaT/2r1b/blob/master/printed_cards.jpg
