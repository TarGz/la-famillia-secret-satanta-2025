#!/usr/bin/env python3
"""
Secret Santa Generator for La Famillia
Generates random matches and individual HTML pages for each participant
"""

import random
import json
import string
import unicodedata
from pathlib import Path


# List of participants (18 individual people)
PARTICIPANTS = [
    "Annie",
    "Jacques",
    "Vincent",
    "Nathalie",
    "Grégoire",
    "Aroldo",
    "Laurence",
    "Patrick",
    "Arthur",
    "Mathilde",
    "Quentin",
    "Clémence",
    "Axel",
    "Julien",
    "Aurélie",
    "Oscar",
    "Jeanne",
    "Léon"
]


def generate_random_string(length=8):
    """Generate a random string of letters and numbers"""
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_filename(name):
    """Convert participant name to filename-friendly format"""
    # Remove accents by normalizing to NFD and filtering out diacritics
    nfd = unicodedata.normalize('NFD', name)
    without_accents = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    # Convert to lowercase and replace spaces with hyphens
    filename_base = without_accents.lower().replace(' ', '-')
    return filename_base


def generate_matches(participants):
    """
    Generate Secret Santa matches ensuring no one gets themselves
    Returns a dictionary mapping giver -> receiver
    """
    receivers = participants.copy()
    givers = participants.copy()
    matches = {}

    # Keep trying until we get a valid matching
    max_attempts = 1000
    for attempt in range(max_attempts):
        random.shuffle(receivers)

        # Check if anyone got themselves
        valid = True
        for i, giver in enumerate(givers):
            if giver == receivers[i]:
                valid = False
                break

        if valid:
            # Create the matching dictionary
            for i, giver in enumerate(givers):
                matches[giver] = receivers[i]
            return matches

    raise Exception("Could not generate valid matching after {} attempts".format(max_attempts))


def create_individual_page(giver, receiver, random_string):
    """Generate HTML for individual participant page"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secret Santa - La Famillia</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 50%, #1a472a 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }}

        /* Snowflakes animation */
        .snowflake {{
            position: absolute;
            top: -10px;
            color: white;
            font-size: 1em;
            font-family: Arial, sans-serif;
            text-shadow: 0 0 5px #fff;
            animation: fall linear infinite;
        }}

        @keyframes fall {{
            to {{
                transform: translateY(100vh);
            }}
        }}

        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            position: relative;
            z-index: 1;
        }}

        .header {{
            margin-bottom: 30px;
        }}

        h1 {{
            color: #c41e3a;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .greeting {{
            font-size: 1.3em;
            color: #2d5a3d;
            margin-bottom: 30px;
        }}

        .reveal-section {{
            margin: 40px 0;
        }}

        .reveal-button {{
            background: linear-gradient(135deg, #c41e3a 0%, #a01729 100%);
            color: white;
            border: none;
            padding: 20px 40px;
            font-size: 1.3em;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(196, 30, 58, 0.4);
            font-weight: bold;
        }}

        .reveal-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(196, 30, 58, 0.6);
        }}

        .reveal-button:active {{
            transform: translateY(0);
        }}

        .revealed {{
            display: none;
            margin-top: 30px;
            padding: 30px;
            background: linear-gradient(135deg, #fff9e6 0%, #ffe6cc 100%);
            border-radius: 15px;
            border: 3px solid #c41e3a;
        }}

        .revealed.show {{
            display: block;
            animation: fadeIn 0.5s ease;
        }}

        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: scale(0.9);
            }}
            to {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        .receiver-name {{
            font-size: 2em;
            color: #c41e3a;
            font-weight: bold;
            margin: 20px 0;
        }}

        .info-section {{
            margin-top: 40px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            text-align: left;
        }}

        .info-section h2 {{
            color: #2d5a3d;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}

        .info-item {{
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
            border-left: 4px solid #c41e3a;
        }}

        .info-item strong {{
            color: #2d5a3d;
        }}

        .rules {{
            margin-top: 20px;
        }}

        .rules ul {{
            list-style: none;
            padding-left: 0;
        }}

        .rules li {{
            padding: 10px;
            margin: 8px 0;
            background: white;
            border-radius: 5px;
            border-left: 4px solid #2d5a3d;
        }}

        .rules li::before {{
            content: "🎁 ";
            margin-right: 10px;
        }}

        .decoration {{
            font-size: 3em;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <!-- Snowflakes -->
    <script>
        // Generate snowflakes
        for (let i = 0; i < 20; i++) {{
            let snowflake = document.createElement('div');
            snowflake.className = 'snowflake';
            snowflake.innerHTML = '❄';
            snowflake.style.left = Math.random() * 100 + '%';
            snowflake.style.animationDuration = (Math.random() * 3 + 2) + 's';
            snowflake.style.animationDelay = Math.random() * 5 + 's';
            snowflake.style.opacity = Math.random();
            snowflake.style.fontSize = (Math.random() * 10 + 10) + 'px';
            document.body.appendChild(snowflake);
        }}
    </script>

    <div class="container">
        <div class="header">
            <div class="decoration">🎄 ⭐ 🎄</div>
            <h1>Secret Santa</h1>
            <h2 style="color: #2d5a3d; margin-top: 10px;">La Famillia 2025</h2>
        </div>

        <p class="greeting">Bonjour <strong>{giver}</strong> !</p>

        <div class="reveal-section">
            <button class="reveal-button" onclick="revealSecretSanta()">
                🎁 Découvre ton Secret Santa 🎁
            </button>

            <div class="revealed" id="revealed">
                <div class="decoration">🎅 🎁 🎅</div>
                <p style="font-size: 1.2em; color: #2d5a3d;">Tu dois offrir un cadeau à :</p>
                <div class="receiver-name">{receiver}</div>
                <div class="decoration">✨ 🌟 ✨</div>
            </div>
        </div>

        <div class="info-section">
            <h2>📅 Informations</h2>
            <div class="info-item">
                <strong>Date :</strong> 25 décembre 2025 (soir)
            </div>
            <div class="info-item">
                <strong>Lieu :</strong> Les Quinaux
            </div>

            <div class="rules">
                <h2 style="margin-top: 25px;">📜 Règles</h2>
                <ul>
                    <li>Cadeau à moins de 50€</li>
                    <li>Le jour même : pense à bien avoir écrit le nom sur le papier cadeau</li>
                    <li>Si tu as une idée de cadeau, n'hésite pas à en faire part à tes proches qui pourraient être contactés pour savoir ce qui te ferait plaisir</li>
                </ul>
            </div>
        </div>

        <div style="margin-top: 30px; color: #888; font-size: 0.9em;">
            <p>🎄 Joyeux Noël et bon Secret Santa ! 🎄</p>
        </div>
    </div>

    <script>
        function revealSecretSanta() {{
            const revealed = document.getElementById('revealed');
            revealed.classList.add('show');

            // Optionally hide the button after reveal
            const button = document.querySelector('.reveal-button');
            button.style.display = 'none';
        }}
    </script>
    <div style="position: fixed; bottom: 5px; right: 10px; font-size: 10px; color: #999; opacity: 0.5;">v1.0.1</div>
</body>
</html>"""

    return html


def create_landing_page():
    """Generate the landing page HTML"""

    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secret Santa - La Famillia 2025</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 50%, #1a472a 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }

        /* Snowflakes animation */
        .snowflake {
            position: absolute;
            top: -10px;
            color: white;
            font-size: 1em;
            font-family: Arial, sans-serif;
            text-shadow: 0 0 5px #fff;
            animation: fall linear infinite;
        }

        @keyframes fall {
            to {
                transform: translateY(100vh);
            }
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            position: relative;
            z-index: 1;
        }

        h1 {
            color: #c41e3a;
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        h2 {
            color: #2d5a3d;
            font-size: 1.8em;
            margin-bottom: 30px;
        }

        .decoration {
            font-size: 4em;
            margin: 20px 0;
        }

        .message {
            font-size: 1.2em;
            color: #555;
            line-height: 1.8;
            margin: 30px 0;
        }

        .info-box {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
            border-left: 5px solid #c41e3a;
        }

        .info-box p {
            color: #333;
            font-size: 1.1em;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <!-- Snowflakes -->
    <script>
        // Generate snowflakes
        for (let i = 0; i < 20; i++) {
            let snowflake = document.createElement('div');
            snowflake.className = 'snowflake';
            snowflake.innerHTML = '❄';
            snowflake.style.left = Math.random() * 100 + '%';
            snowflake.style.animationDuration = (Math.random() * 3 + 2) + 's';
            snowflake.style.animationDelay = Math.random() * 5 + 's';
            snowflake.style.opacity = Math.random();
            snowflake.style.fontSize = (Math.random() * 10 + 10) + 'px';
            document.body.appendChild(snowflake);
        }
    </script>

    <div class="container">
        <div class="decoration">🎄 ⭐ 🎄</div>
        <h1>Secret Santa</h1>
        <h2>La Famillia 2025</h2>

        <p class="message">
            Bienvenue au Secret Santa de La Famillia !
        </p>

        <div class="decoration">🎅 🎁 🎅</div>

        <div class="info-box">
            <p><strong>📅 Date :</strong> 25 décembre 2025 (soir)</p>
            <p><strong>📍 Lieu :</strong> Les Quinaux</p>
        </div>

        <p class="message" style="margin-top: 30px; font-size: 1em; color: #888;">
            Tu as normalement reçu un lien personnalisé, si tu ne l'as pas contacte Julien : <a href="mailto:julien@terraz.org" style="color: #c41e3a; text-decoration: none;">julien@terraz.org</a>
        </p>

        <div class="decoration" style="font-size: 2em; margin-top: 30px;">
            ✨ 🌟 ✨
        </div>
    </div>
    <div style="position: fixed; bottom: 5px; right: 10px; font-size: 10px; color: #999; opacity: 0.5;">v1.0.1</div>
</body>
</html>"""

    return html


def main():
    """Main function to generate all Secret Santa files"""

    print("🎄 Secret Santa Generator for La Famillia 🎄\n")

    # Output directory is current directory (root)
    output_dir = Path(".")

    # Generate matches
    print("Generating Secret Santa matches...")
    matches = generate_matches(PARTICIPANTS)

    # Generate unique URLs and mapping
    url_mapping = {}

    print("\nGenerating HTML pages...")

    for giver, receiver in matches.items():
        # Generate random string for URL
        random_string = generate_random_string()

        # Create filename
        filename_base = generate_filename(giver)
        filename = f"{filename_base}-{random_string}.html"

        # Store mapping
        url_mapping[giver] = {
            "receiver": receiver,
            "filename": filename,
            "url": f"https://targz.github.io/secret-santa-2025/{filename}"
        }

        # Generate and save HTML
        html_content = create_individual_page(giver, receiver, random_string)
        output_file = output_dir / filename
        output_file.write_text(html_content, encoding='utf-8')

        print(f"✓ Created: {filename}")

    # Create landing page
    print("\nCreating landing page...")
    index_html = create_landing_page()
    (output_dir / "index.html").write_text(index_html, encoding='utf-8')
    print("✓ Created: index.html")

    # Note: JSON mapping file generation has been disabled to prevent overwriting
    # The original mapping file is protected and should not be regenerated
    print("\n⚠️  JSON mapping file generation disabled (to protect existing matches)")

    # Print summary
    print("\n" + "="*60)
    print("✅ Generation complete!")
    print("="*60)
    print(f"\nFiles generated in current directory:")
    print(f"  - index.html (landing page)")
    print(f"  - {len(matches)} individual participant pages")
    print("\n📧 URLs to distribute:")
    print("-" * 60)

    for giver in sorted(url_mapping.keys()):
        info = url_mapping[giver]
        print(f"{giver:25} → {info['url']}")

    print("\n🎁 Joyeux Noël et bon Secret Santa! 🎁")


if __name__ == "__main__":
    main()
