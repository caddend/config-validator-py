import configparser
import sys
import os

REQUIRED_SECTIONS = ['database', 'logging']
REQUIRED_KEYS = {
    'database': ['host', 'port', 'user'],
    'logging': ['level']
}

def validate_config(file_path):
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл не найден по пути {file_path}")
        return False

    config = configparser.ConfigParser()
    try:
        config.read(file_path)
    except configparser.Error as e:
        print(f"Ошибка парсинга файла {file_path}: {e}")
        return False

    validation_passed = True
    print(f"--- Отчет валидации для {file_path} ---")

    # 1. Проверка секций
    missing_sections = [s for s in REQUIRED_SECTIONS if s not in config]
    if missing_sections: 
        print(f"[ОШИБКА] Отсутствуют обязательные секции: {', '.join(missing_sections)}")
        validation_passed = False
    else:
        print("[УСПЕХ] Все обязательные секции присутствуют.")

    # 2. Проверка ключей и типов
    for section in REQUIRED_SECTIONS:
        if section in config:
            expected_keys = REQUIRED_KEYS[section]
            present_keys = config.options(section)
            
            missing_keys = [k for k in expected_keys if k not in present_keys]
            if missing_keys:
                print(f"[ОШИБКА] В секции [{section}] отсутствуют ключи: {', '.join(missing_keys)}")
                validation_passed = False
            else:
                print(f"[УСПЕХ] Все обязательные ключи в секции [{section}] присутствуют.")

                # Проверка типов (базовая: port должен быть числом)
                if section == 'database' and 'port' in present_keys:
                    try:
                        port = int(config.get(section, 'port'))
                        if port <= 0: raise ValueError
                        print(f"[УСПЕХ] Тип 'port' в [{section}] корректен (число > 0).")
                    except ValueError:
                        print(f"[ОШИБКА] Тип 'port' в [{section}] должен быть целым числом.")
                        validation_passed = False

    print("----------------------------------")
    if validation_passed:
        print("✅ Конфигурационный файл прошел валидацию.")
    else:
        print("❌ Конфигурационный файл НЕ прошел валидацию. Исправьте ошибки выше.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python validator.py <путь_к_конфигурационному_файлу.ini>")
        sys.exit(1)
    
    config_file_path = sys.argv[1]
    validate_config(config_file_path)
