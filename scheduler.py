import schedule
import time
import logging
import os
from datetime import datetime
from travel import run as run_travel
from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

if not os.path.exists('logs'):
    os.makedirs('logs')


def run_test():
    """Run the travel insurance test"""
    logger.info("=" * 80)
    logger.info(f"Starting scheduled test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    try:
        with sync_playwright() as playwright:
            run_travel(playwright)
        logger.info("Test completed successfully!")
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
    
    logger.info("=" * 80)
    logger.info("")


def main():
    """Main scheduler function"""
    logger.info("=" * 80)
    logger.info("Travel Insurance Test Automation Scheduler Started")
    logger.info(f"Tests will run every 1 hour")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'production')}")
    logger.info("=" * 80)
    logger.info("")
    
    logger.info("Running initial test on startup...")
    run_test()
    
    schedule.every(1).hour.do(run_test)
    
    logger.info("Scheduler initialized - Next run in 1 hour")
    logger.info("=" * 80)
    logger.info("")
    
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()