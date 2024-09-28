import argparse
import asyncio
import logging
from aiopath import AsyncPath
from aioshutil import copyfile


async def read_folder(path: AsyncPath) -> None:                     # Асинхронно читаємо усі файли у папці та її сабпапках
                                                                    # викликаємо функцію copy_file для кожного файлу.
    async for item in path.rglob('*'):                              # Рекурсивно шукаємо всі файли та папки
        if await item.is_file():                                    # Якщо знайдено файл
            logging.info(f"Found file: {item}")
            await copy_file(item)                                   # Копіюємо файл асинхронно


async def copy_file(file: AsyncPath) -> None:                       # Асинхронно копіюємо файл до сабпапки згідно з його розширенням
    try:
        extension_name = file.suffix[1:]                            # Отримуємо розширення файлу без крапки
        extension_folder = output / extension_name                  # Визначаємо цільову папку
        await extension_folder.mkdir(exist_ok=True, parents=True)   # Створюємо підпапку, якщо її ще немає
        await copyfile(file, extension_folder / file.name)          # Копіюємо файл до підпапки
        logging.info(f"Copied {file} to {extension_folder}")
    except Exception as e:
        logging.error(f"Error copying {file}: {e}")                 # Логуємо помилки, якщо виникають


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s") # Налаштуваємо логування

    parser = argparse.ArgumentParser(description="Sort files by extension")                 # Створюємо об'єкт ArgumentParser 
    parser.add_argument("source", type=str, help="Path to the source folder")
    parser.add_argument("output", type=str, help="Path to the output folder")
    
    args = parser.parse_args()

    source = AsyncPath(args.source)                                 # Призначаємо шляхи для вихідної (source)
    global output
    output = AsyncPath(args.output)                                 # та цільової папок

    asyncio.run(read_folder(source))                                # Запускаємо асинхронну функцію для обробки файлів
