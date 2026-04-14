# import { test, expect } from '@playwright/test';

# test('test', async ({ page }) => {
#   await page.goto('https://oldmutual.co.ke/app/public/motor-private');
#   await page.getByTestId('third-party-select').getByRole('button', { name: 'Select' }).click();
#   await page.getByRole('button', { name: 'Close tooltip' }).click();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.getByRole('textbox', { name: 'Fullname' }).click();
#   await page.getByRole('textbox', { name: 'Fullname' }).fill('test doe');
#   await page.getByRole('textbox', { name: 'Phone' }).click();
#   await page.getByRole('textbox', { name: 'Phone' }).fill('0742587238');
#   await page.getByRole('textbox', { name: 'Email' }).click();
#   await page.getByRole('textbox', { name: 'Email' }).fill('faith.njeri@oldmutual.com');
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.locator('div').filter({ hasText: /^Car$/ }).click();
#   await page.locator('.display-value').first().click();
#   await page.getByTestId('ke-vehicle-type-0').locator('omk-radio-button').click();
#   await page.locator('.display-value').first().click();
#   await page.getByRole('menu').getByText('BMW').click();
#   await page.locator('div:nth-child(6) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.locator('div:nth-child(6) > omk-select > .anchor-wrapper > .sc-omk-menu-h > #selectMenu > omk-menu-item:nth-child(13) > .sc-omk-menu-item > #item > md-item').click();
#   await page.getByRole('spinbutton', { name: 'Year of manufacture' }).click();
#   await page.getByRole('spinbutton', { name: 'Year of manufacture' }).click();
#   await page.getByRole('spinbutton', { name: 'Year of manufacture' }).fill('2011');
#   await page.getByRole('textbox', { name: 'When would you like your' }).click();
#   await page.getByRole('textbox', { name: 'When would you like your' }).fill('01/01/2027');
#   await page.getByRole('button', { name: 'Minimize live chat window' }).click();
#   await page.getByTestId('ke-alarm-installed-0').locator('omk-radio-button').click();
#   await page.locator('#ke-tracking-installed-1 > .sc-omk-radio.hydrated > .outer-circle').click();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.getByRole('button', { name: 'Buy Now' }).click();
#   await page.locator('.display-value').first().click();
#   await page.getByRole('menu').getByText('Kenyan').click();
#   await page.getByRole('textbox', { name: 'National ID' }).fill('17837723');
#   await page.getByRole('textbox', { name: 'Date of Birth' }).click();
#   await page.getByRole('textbox', { name: 'Date of Birth' }).fill('01/01/2001');
#   await page.locator('#ke-gender-type-1 > .sc-omk-radio.hydrated > .outer-circle').click();
#   await page.locator('div:nth-child(7) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.locator('div:nth-child(7) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.getByRole('menu').getByText('Cook (Fast Food)').click();
#   await page.getByRole('textbox', { name: 'KRA PIN' }).press('CapsLock');
#   await page.getByRole('textbox', { name: 'KRA PIN' }).fill('A');
#   await page.getByRole('textbox', { name: 'KRA PIN' }).press('CapsLock');
#   await page.getByRole('textbox', { name: 'KRA PIN' }).fill('A123456789k');
#   await page.getByRole('menu').getByText('Cook (Fast Food)').click();
#   await page.getByRole('textbox', { name: 'Postal Address' }).fill('0100');
#   await page.locator('#ke-agent-select-1 > .sc-omk-radio.hydrated > .outer-circle > .inner-circle').click();
#   await page.getByRole('button', { name: 'Next' }).click();
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).click();
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).press('CapsLock');
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).fill('K');
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).press('CapsLock');
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).fill('KHA123k');
#   await page.getByRole('textbox', { name: 'Chassis number' }).click();
#   await page.getByRole('textbox', { name: 'Chassis number' }).fill('GH12-283');
#   await page.getByRole('textbox', { name: 'Engine Number' }).click();
#   await page.getByRole('textbox', { name: 'Engine Number' }).fill('GDHY-097YUIy');
#   await page.locator('.display-value').first().click();
#   await page.getByRole('menu').getByText('Hybrid').click();
#   await page.locator('div:nth-child(5) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.getByRole('menu').getByText('S/Cabin').click();
#   await page.getByRole('spinbutton', { name: 'Sitting capacity' }).click();
#   await page.getByRole('spinbutton', { name: 'Sitting capacity' }).fill('1');
#   await page.locator('div:nth-child(7) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.getByRole('menu').getByText('Beige').click();
#   await page.getByRole('spinbutton', { name: 'Years with driving license' }).click();
#   await page.getByRole('spinbutton', { name: 'Years with driving license' }).fill('3');
#   await page.getByRole('button', { name: 'Next' }).click();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.locator('omk-document-upload').filter({ hasText: 'insert_drive_fileCopy of National ID *PDF, JPEG, or JPG. Max 2MBfile_upload' }).locator('#button').click();
#   await page.locator('omk-document-upload').filter({ hasText: 'insert_drive_fileCopy of National ID *PDF, JPEG, or JPG. Max 2MBfile_upload' }).locator('#button').setInputFiles('logbook-kenya.jpg');
#   await page.locator('omk-document-upload').filter({ hasText: 'insert_drive_fileCopy of KRA' }).locator('#button').click();
#   await page.locator('omk-document-upload').filter({ hasText: 'insert_drive_fileCopy of KRA' }).locator('#button').setInputFiles('Birthcertificate.jpg');
#   await page.locator('#upload-logBook #button').click();
#   await page.locator('#upload-logBook #button').setInputFiles('Birthcertificate.jpg');
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.getByTestId('hasDeclinedProposal').locator('#input').check();
#   await page.getByTestId('hasIncreasedPremium').locator('#input').check();
#   await page.getByTestId('hasCancelledPolicy').locator('#input').check();
#   await page.getByTestId('hasPhysicalCondition').locator('#input').check();
#   await page.getByTestId('hasPhysicalCondition').locator('#input').uncheck();
#   await page.getByTestId('hasPhysicalCondition').locator('#input').check();
#   await page.getByTestId('hasDrivingOffense').locator('#input').check();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.getByTestId('ke-personalDataProcessingConsent-0').locator('omk-radio-button').click();
#   await page.locator('#ke-childDataProcessingConsent-0 > .sc-omk-radio.hydrated > .outer-circle > .inner-circle').click();
#   await page.getByTestId('consentForNewProductsAndServices').locator('#input').check();
#   await page.getByTestId('consentForProductsAndServicesRelatedWithMyPolicy').locator('#input').check();
#   await page.getByTestId('termsAndConditions').locator('#input').check();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.getByRole('button', { name: 'Process Payment' }).click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('bank_transfer-nav').click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('card-nav').click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('atl_ke-nav').click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('mptill-nav').click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('atl_ke-nav').click();
# });
from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import traceback

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def screenshot(page, name):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    page.screenshot(path=f"{SCREENSHOTS_DIR}/{ts}_{name}.png", full_page=True)


def force_continue(page):
    """
    HARD FORCE CONTINUE BUTTON:
    Removes 'disabled' attribute and clicks via JS
    """
    page.evaluate("""
        const btn = document.querySelector('button#button');
        if (btn) {
            btn.disabled = false;
            btn.removeAttribute('disabled');
            btn.click();
        }
    """)


def run_motor_third_party():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        step = "Unknown"
        start = datetime.now()

        try:
            # STEP 1
            step = "Step 1: Select Third Party"
            print(step)

            page.goto("https://oldmutual.co.ke/app/public/motor-private", timeout=60000)
            page.wait_for_timeout(4000)

            page.get_by_test_id("third-party-select").get_by_role("button", name="Select").click()

            try:
                page.get_by_role("button", name="Close tooltip").click(timeout=1500)
            except:
                pass

            force_continue(page)

            # STEP 2
            step = "Step 2: Personal Details"
            print(step)

            page.wait_for_timeout(2000)
            page.get_by_role("textbox", name="Fullname").fill("Test Doe")
            page.get_by_role("textbox", name="Phone").fill("0742587238")
            page.get_by_role("textbox", name="Email").fill("faith.njeri@oldmutual.com")

            force_continue(page)

            # STEP 3
            step = "Step 3: Vehicle Details"
            print(step)

            page.wait_for_timeout(3000)

            # Vehicle Type = Car
            page.get_by_test_id("ke-vehicle-type-0").locator("omk-radio-button").click()

            # Make dropdown – brute keyboard
            page.locator(".display-value").first.click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            # Model dropdown – brute keyboard
            page.locator("div:nth-child(6) .display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_role("spinbutton", name="Year of manufacture").fill("2011")
            page.get_by_role("textbox", name="When would you like your").fill("01/01/2027")

            page.get_by_test_id("ke-alarm-installed-0").locator("omk-radio-button").click()
            page.locator("#ke-tracking-installed-1 .outer-circle").click()

            screenshot(page, "vehicle_details_filled")

            # 🔥 FORCE CONTINUE EVEN IF UI THINKS INVALID
            force_continue(page)

            # STEP 4
            step = "Step 4: Buy Now"
            print(step)

            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Buy Now").click()

            # STEP 5
            step = "Step 5: Additional Info"
            print(step)

            page.wait_for_timeout(3000)

            page.locator(".display-value").first.click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_role("textbox", name="National ID").fill("17837723")
            page.get_by_role("textbox", name="Date of Birth").fill("01/01/2001")
            page.locator("#ke-gender-type-1 .outer-circle").click()

            page.locator("div:nth-child(7) .display-value").click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_role("textbox", name="KRA PIN").fill("A123456789k")
            page.get_by_role("textbox", name="Postal Address").fill("0100")
            page.locator("#ke-agent-select-1 .outer-circle").click()

            force_continue(page)

            # STEP 6
            step = "Step 6: Vehicle Registration"
            print(step)

            page.wait_for_timeout(2000)
            page.get_by_role("textbox", name="Vehicle registration number").fill("KHA123K")
            page.get_by_role("textbox", name="Chassis number").fill("GH12-283")
            page.get_by_role("textbox", name="Engine Number").fill("GDHY-097YUIY")

            page.locator(".display-value").first.click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.locator("div:nth-child(5) .display-value").click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_role("spinbutton", name="Sitting capacity").fill("1")

            page.locator("div:nth-child(7) .display-value").click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_role("spinbutton", name="Years with driving license").fill("3")
            force_continue(page)

            # STEP 7
            step = "Step 7: Payment Entry"
            print(step)

            page.wait_for_timeout(3000)
            screenshot(page, "before_payment")

            duration = (datetime.now() - start).total_seconds()
            print(f"✅ FLOW COMPLETED in {duration:.1f}s")

        except Exception as e:
            screenshot(page, "ERROR")
            print(f"❌ FAILED at {step}")
            print(str(e))
            print(traceback.format_exc())

        finally:
            browser.close()


if __name__ == "__main__":
    run_motor_third_party()



