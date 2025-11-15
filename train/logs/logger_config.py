"""
Configuração centralizada de logging para o projeto MLOps.
"""

import logging
import os
from pathlib import Path


def setup_logger(
    name: str = __name__,
    log_file: str = 'train/logs/app.log',
    level: int = logging.INFO,
    file_mode: str = 'w'
) -> logging.Logger:
    """
    Configura e retorna um logger que escreve tanto no console quanto em arquivo.
    
    Args:
        name: Nome do logger
        log_file: Caminho do arquivo de log
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        file_mode: Modo de abertura do arquivo ('w' para sobrescrever, 'a' para append)
    
    Returns:
        Logger configurado
    """
    
    # Cria o logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove handlers existentes para evitar duplicação
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Formato das mensagens
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Garante que o diretório do arquivo de log existe
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, mode=file_mode)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Handler para console (tela)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Adiciona os handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Retorna um logger já configurado.
    Se não existir, cria um novo com configuração padrão.
    
    Args:
        name: Nome do logger
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Se o logger não tem handlers, configura ele
    if not logger.hasHandlers():
        return setup_logger(name)
    
    return logger
