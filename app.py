from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os
import atexit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
import os


# Configurações do servidor de email (exemplo com Gmail)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'qrcodemastercombr@gmail.com'  # Substitua pelo seu email
SMTP_PASSWORD = 'xxlh iwcq pxez bwvn'  # Substitua pela sua senha


app = Flask(__name__)
app.secret_key = 'c324e85fce3df8bbb53be952ca0475dead443e8490adf2bf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'  # Pasta para armazenar imagens
db = SQLAlchemy(app)

POSTS_PER_PAGE = 5

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    scheduled_time = db.Column(db.DateTime, nullable=True)
    posted = db.Column(db.Boolean, default=False)

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    
class AffiliateProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False, unique=True)
    affiliate_link = db.Column(db.String(200), nullable=False)

# Use o contexto da aplicação para criar o banco de dados
with app.app_context():
    db.create_all()

def send_email(subject, body, to_emails):
    # Configuração do servidor SMTP (exemplo com Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'qrcodemastercombr@gmail.com'
    smtp_password = 'xxlh iwcq pxez bwvn'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = ', '.join(to_emails)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_emails, msg.as_string())
        
        
@app.route('/send_mass_email', methods=['GET', 'POST'])
def send_mass_email():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image = request.files.get('image')

        # Lê os emails do arquivo CSV
        csv_file = 'subscribers.csv'
        if not os.path.exists(csv_file):
            flash("Arquivo CSV de assinantes não encontrado.")
            return redirect(url_for('send_mass_email'))

        emails = read_emails_from_csv(csv_file)

        # Envia email para cada inscrito
        for email in emails:
            send_email(email, title, message, image)

        flash('Emails enviados com sucesso!')
        return redirect(url_for('send_mass_email'))

    return render_template('send_email.html')

def read_emails_from_csv(csv_file):
    """Lê os emails do arquivo CSV e retorna uma lista de emails."""
    emails = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            emails.append(row['Email'])
    return emails

def send_email(to_email, subject, message, image=None):
    """Envia um email individual para o destinatário."""
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject

    # Adiciona o corpo da mensagem
    msg.attach(MIMEText(message, 'plain'))

    # Se houver uma imagem, anexar a imagem ao email
    if image:
        image_data = image.read()  # Lê o conteúdo do arquivo da imagem
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(image_data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={image.filename}')
        msg.attach(part)

    # Envia o email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        
        
def publish_scheduled_posts():
    with app.app_context():
        now = datetime.now()
        scheduled_posts = Post.query.filter(Post.scheduled_time <= now, Post.posted == False).all()
        for post in scheduled_posts:
            post.posted = True
            db.session.commit()
            send_newsletter(post)

def send_newsletter(post):
    subscribers = Subscriber.query.all()
    to_emails = [subscriber.email for subscriber in subscribers]
    subject = f"Novo Conteúdo Postado: {post.title}"
    body = f"Confira o novo conteúdo postado: {post.title}\n\n{post.content}\n\nAcesse o site para mais detalhes!"
    send_email(subject, body, to_emails)


scheduler = BackgroundScheduler()
scheduler.add_job(func=publish_scheduled_posts, trigger="interval", minutes=1)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        scheduled_time = datetime.strptime(request.form['scheduled_time'], '%Y-%m-%dT%H:%M')

        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            image_url = image_path
        else:
            image_url = None

        # Automatiza a adição de links de afiliados no conteúdo
        content_with_affiliates = add_affiliate_links(content)

        new_post = Post(title=title, content=content_with_affiliates, image_url=image_url, scheduled_time=scheduled_time)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('admin'))

    # Obtém todas as publicações para exibir no admin, sem paginação
    posts = Post.query.order_by(Post.scheduled_time).all()
    return render_template('admin.html', posts=posts)

def add_affiliate_links(content):
    """Adiciona links de afiliados automaticamente ao conteúdo."""
    products = AffiliateProduct.query.all()
    for product in products:
        # Somente substitui o nome exato do produto pelo link de afiliado
        content = replace_exact_word(content, product.product_name, f'<a href="{product.affiliate_link}" target="_blank">{product.product_name}</a>')
    return content

def replace_exact_word(text, word, replacement):
    """Substitui apenas a palavra exata no texto, respeitando capitalização."""
    import re
    # Expressão regular para correspondência exata da palavra, ignorando maiúsculas/minúsculas
    def replacement_function(match):
        return replacement

    pattern = r'\b{}\b'.format(re.escape(word))
    # Usa re.sub com uma função de substituição para aplicar o link
    return re.sub(pattern, replacement_function, text, flags=re.IGNORECASE)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        image = request.files['image']
        post.scheduled_time = datetime.strptime(request.form['scheduled_time'], '%Y-%m-%dT%H:%M')

        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            post.image_url = image_path
        
        post.content = add_affiliate_links(post.content)

        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(posted=True).order_by(Post.scheduled_time.desc()).paginate(page=page, per_page=POSTS_PER_PAGE)
    return render_template('index.html', posts=posts)

@app.route('/teste')
def teste():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(posted=True).order_by(Post.scheduled_time.desc()).paginate(page=page, per_page=POSTS_PER_PAGE)
    return render_template('index.html', posts=posts)

@app.route('/teste2')
def teste2():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(posted=True).order_by(Post.scheduled_time.desc()).paginate(page=page, per_page=POSTS_PER_PAGE)
    return render_template('index.html', posts=posts)

@app.route('/teste2')
def teste2():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(posted=True).order_by(Post.scheduled_time.desc()).paginate(page=page, per_page=POSTS_PER_PAGE)
    return render_template('index.html', posts=posts)


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form['email']
        if not Subscriber.query.filter_by(email=email).first():
            new_subscriber = Subscriber(email=email)
            db.session.add(new_subscriber)
            db.session.commit()
            flash('Inscrição realizada com sucesso!')
            
              # Salva no arquivo CSV
            save_email_to_csv(email)
        else:
            flash('Este e-mail já está inscrito.')

        return redirect(url_for('index'))

    return render_template('subscribe.html')


def save_email_to_csv(email):
    """Salva o email inscrito no arquivo CSV."""
    # Define o nome do arquivo CSV
    csv_file = 'subscribers.csv'

    # Verifica se o arquivo já existe
    file_exists = os.path.isfile(csv_file)

    # Abre o arquivo no modo de 'append' para adicionar sem sobrescrever
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Se o arquivo for criado agora, adiciona o cabeçalho
        if not file_exists:
            writer.writerow(['Email'])  # Cabeçalho do arquivo CSV

        # Escreve o email no arquivo CSV
        writer.writerow([email])

@app.route('/affiliates', methods=['GET', 'POST'])
def affiliates():
    if request.method == 'POST':
        product_name = request.form['product_name']
        affiliate_link = request.form['affiliate_link']

        # Adiciona o novo produto de afiliado ao banco de dados
        new_product = AffiliateProduct(product_name=product_name, affiliate_link=affiliate_link)
        db.session.add(new_product)
        db.session.commit()

        flash('Produto de afiliado adicionado com sucesso!')

    products = AffiliateProduct.query.all()
    return render_template('affiliates.html', products=products)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/politica')
def politica():
    return render_template('politica.html')

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8024)
