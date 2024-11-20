from flask import Flask, render_template, request, jsonify
import os
import subprocess
import shlex
import datetime

app = Flask(__name__)
BACKUP_FOLDER = "/data"  # Imposta la directory dei backup

@app.route('/')
def index():
    """Rende la pagina principale con l'elenco dei backup disponibili."""
    backups = [f for f in os.listdir(BACKUP_FOLDER) if f.endswith('.sql')]
    return render_template('index.html', backups=backups)

@app.route('/backup', methods=['POST'])
def backup():
    """Crea un backup dei database MySQL."""
    host = request.form.get('host')  # Parametro host
    user = request.form.get('user')
    password = request.form.get('password')
    filename_db = request.form.get('filename_db')
    filename_config = request.form.get('filename_config')

    if not host or not user or not password or not filename_db or not filename_config:
        return jsonify({'status': 'error', 'message': 'Tutti i campi sono obbligatori'}), 400

    filepath_db = os.path.join(BACKUP_FOLDER, filename_db)
    filepath_config = os.path.join(BACKUP_FOLDER, filename_config)

    # Genera il nome del file di log
    log_filename = os.path.join(BACKUP_FOLDER, f"backup_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Comando per il backup del database completo
    cmd_db = f"mysqldump -h {host} -u {user} -p{password} --all-databases > {filepath_db}"
    # Comando per il backup della configurazione (senza dati)
    cmd_config = f"mysqldump -h {host} -u {user} -p{password} --no-data --all-databases --routines --triggers --events > {filepath_config}"

    try:
        # Esegui il comando e cattura output e errori
        app.logger.debug(f"Comando di backup DB: {cmd_db}")
        result_db = subprocess.run(cmd_db, shell=True, text=True, capture_output=True)
        
        app.logger.debug(f"Comando di backup Config: {cmd_config}")
        result_config = subprocess.run(cmd_config, shell=True, text=True, capture_output=True)

        # Scrivi gli output nel log
        with open(log_filename, 'w') as log_file:
            log_file.write(f"Comando eseguito per backup DB: {cmd_db}\n")
            log_file.write(f"Stdout DB:\n{result_db.stdout}\n")
            log_file.write(f"Stderr DB:\n{result_db.stderr}\n")
            
            log_file.write(f"Comando eseguito per backup Config: {cmd_config}\n")
            log_file.write(f"Stdout Config:\n{result_config.stdout}\n")
            log_file.write(f"Stderr Config:\n{result_config.stderr}\n")
            
            if result_db.returncode == 0 and result_config.returncode == 0:
                log_file.write("Backup completato con successo\n")
            else:
                log_file.write(f"Errore durante il backup DB (codice: {result_db.returncode})\n")
                log_file.write(f"Errore durante il backup Config (codice: {result_config.returncode})\n")

        # Log degli errori se ci sono
        if result_db.stderr or result_config.stderr:
            app.logger.error(f"Errori durante il backup DB: {result_db.stderr}")
            app.logger.error(f"Errori durante il backup Config: {result_config.stderr}")
        
        # Restituisci il risultato se il comando è andato a buon fine
        result_db.check_returncode()
        result_config.check_returncode()
        
        return jsonify({
            'status': 'success',
            'message': f'Backup completato: {filename_db}, {filename_config}'
        }), 200
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Errore durante il backup: {str(e)}")
        
        # In caso di errore, scrivi l'errore nel file di log
        with open(log_filename, 'a') as log_file:
            log_file.write(f"Errore durante il backup: {str(e)}\n")
        
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/restore', methods=['POST'])
def restore():
    """Ripristina un backup MySQL."""
  
    restore_host = request.form.get('restoreHost')  # Host di ripristino
    restore_host_custom = request.form.get('restoreHostCustom')  # Host personalizzato se presente
    restore_user = request.form.get('restoreUser')  # Nome utente MySQL
    restore_password = request.form.get('restorePassword')  # Password MySQL
    file_to_restore = request.files.get('file')  # File di backup

    # Se l'utente ha scelto "custom", usa il valore dell'host personalizzato
    if restore_host == "custom" and restore_host_custom:
        restore_host = restore_host_custom
    elif not restore_host:
        return jsonify({'status': 'error', 'message': 'Host di ripristino obbligatorio'}), 400

    if not restore_user or not restore_password or not file_to_restore:
        return jsonify({'status': 'error', 'message': 'Utente MySQL, password e file obbligatori'}), 400

    filepath = os.path.join(BACKUP_FOLDER, file_to_restore.filename)
    file_to_restore.save(filepath)  # Salva il file sul server

    # Genera il nome del file di log
    log_filename = os.path.join(BACKUP_FOLDER, f"restore_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Comando per il ripristino
    cmd = f"mysql -h {restore_host} -u {restore_user} -p{restore_password} --force < {filepath}"

    try:
        # Esegui il comando e cattura output e errori
        app.logger.debug(f"Comando di ripristino: {cmd}")
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        
        # Scrivi gli output nel log
        with open(log_filename, 'w') as log_file:
            log_file.write(f"Comando eseguito: {cmd}\n")
            log_file.write(f"Stdout:\n{result.stdout}\n")
            log_file.write(f"Stderr:\n{result.stderr}\n")
            
            if result.returncode == 0:
                log_file.write("Ripristino completato con successo\n")
            else:
                log_file.write(f"Errore durante il ripristino (codice: {result.returncode})\n")
        
        # Log degli errori se ci sono
        if result.stderr:
            app.logger.error(f"Errori ignorati durante il ripristino: {result.stderr}")
        
        # Restituisci il risultato se il comando è andato a buon fine
        result.check_returncode()
        
        return jsonify({'status': 'success', 'message': f'Restore completato da {file_to_restore.filename}'}), 200
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Errore durante il ripristino: {str(e)}")
        
        # In caso di errore, scrivi l'errore nel file di log
        with open(log_filename, 'a') as log_file:
            log_file.write(f"Errore durante il ripristino: {str(e)}\n")
        
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/list-backups", methods=["GET"])
def list_backups():
    """Restituisce l'elenco dei file di backup disponibili."""
    files = [f for f in os.listdir(BACKUP_FOLDER) if f.endswith(".sql")]
    return jsonify({"success": True, "files": files})

if __name__ == '__main__':
    # Crea la cartella di backup se non esiste
    os.makedirs(BACKUP_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
