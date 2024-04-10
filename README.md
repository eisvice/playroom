# Lazy Accountant
## Distinctiveness and Complexity
### Distinctiveness and Complexity

**Distinctive Features:**

1. **Customized Customer Logging:** I offer businesses the ability to quickly log customers by selecting their type and gender, providing a personalized experience from the moment they enter the playroom. This level of customization enhances user engagement and streamlines the logging process.

2. **Real-time Timer and Avatar Display:** Upon logging a customer, I dynamically display their avatar along with a countdown timer directly inside. This feature not only adds visual appeal but also provides real-time tracking of customer duration, enhancing transparency and accountability.

3. **Interactive Modal for Customer Editing:** Users can easily edit customer details such as name, type, gender, and payment method through an interactive modal window. This feature promotes flexibility and adaptability, allowing businesses to accommodate changes on the fly without interrupting operations.

4. **Automatic Notification for New Employees:** I automatically notify the owner about new employees awaiting authorization, ensuring efficient onboarding and seamless integration into the team. This feature enhances collaboration and communication within the organization.

**Complexity Considerations:**

1. **Asynchronous Data Handling:** I leverage asynchronous requests and responses using technologies like htmx, vanillaJS and Django to ensure seamless data synchronization between the frontend and backend. This approach enhances responsiveness and scalability, enabling my app to handle concurrent user interactions efficiently.

2. **Dynamic Data Visualization:** I utilize advanced data visualization techniques, including Chart.js integration, to present complex statistics such as monthly revenue and customer distribution. These dynamic visualizations offer valuable insights at a glance, empowering businesses to make informed decisions and optimize performance.

3. **Pagination and Data Filtering:** I implement pagination and data filtering functionalities using Django Paginator to manage large datasets effectively. This ensures smooth navigation and enhances user experience, especially when browsing through extensive customer logs and statistical reports.

4. **Role-based Access Control:** I feature role-based access control, allowing owners to manage employee permissions and restrict access to sensitive functionalities. This sophisticated authorization mechanism enhances security and confidentiality, safeguarding critical business data and operations.

In this projects my tech stack was Django, SQLite, Javascript and HTMX. In summary, my customer logging app stands out for its user-centric and minimalistic design. 

## Created Files

### HTML Files
1. **layout.html**: file that defines the layout of the entire site. Contains information about plug-in frameworks, libraries, static files, as well as defines the general navigation bar.
1. **index.html**: my main page from where the customer log is taken. it also includes `buttongroup.html`, `customer-form.html`, `customer.html` and `customers.html files`. The division into blocks of files was made for correct work of *htmx*.
1. **history.html**: detailed history of income by day. Contains `history-list.html` and `history-detail.html`files.
1. **charts.html**: page with charts.
1. **notifications.html**: page with information about the company's current and potential employees.
1. **register.html**: page for signing up.
1. **login.html**: page for logging in.

### JS Files
1. **timer.js**: a JavaScript that serves to create dynamically updating content, control multimedia.

### CSS Files
1. **styles.css**: a file to style Web pages.

### Folders
1. **/static/customers**: contains `styles.css` and `timer.js` files.
1. **/static/images**: contains images which are used on the Web site.
1. **/static/sounds**: contains sound samples for audio effects on the Web site.

## Run Application
**INDEX**: The main page gives the user **only four buttons**: select the type of customer and their gender. When a specific customer is selected, the new customer's avatar appears in the container below with the title *Kids in the playing room* and starts a **timer** (1 minute by default to simplify testing), which is displayed directly inside the customer's avatar, and for better visualization fills **the avatar's background with green as the timer expires (when finished, the background will turn coral and play an audio signal)**. By default, a customer name is assigned based on the customer type and the payment method is assigned as cash. If necessary, you can click on the avatar and in the pop-up **modal** you can change the fields of name, type, gender, payment method (**if you pay by bank card, the field with bank selection will become available**), timer duration (the completion time field will change). When you save the changed parameters, the data will be sent **asynchronously to the server** and the changes will be applied to this customer. Also, without entering the **modal**, you can increase the time of stay in the room by one hour and delete the customer using the buttons to the left and right of the customer's name respectively. When the timer expires, the delete button will be replaced by the finish button thanks to **eventListener**. Adding a new customer, removing and ending the timer of each customer is done using the **out of band swap** method by the **htmx** framework, so there is not a complete reload of the page, but *only a certain block of html is rendered*.

**DAILY HISTORY**: The page with daily history with **Django Paginator** and **htmx trigger *reveal*** displays the five most recent active dates and the total income as you scroll down the page. For each date, *a table with a block of customers* is rendered using **htmx trigger *load*** when the load completes. When you click on the pencil icon next to a customer, **JavaScript will display a form** to change the payment amount and payment method. When saving the data, **only the block with the table for a particular day will be replaced without reloading the page**.

**STATISTICS**: On the page with statistics, you will see two canvases. The first one shows the monthly revenue by day, the second one shows the distribution of customers by type and gender. **ChartJS** library was used for this purpose. If you hover over each bar or sector, you can see more detailed information. If there is no day in the database, it is assigned 0. **You can view statistics for each month** of the playroom (by clicking on the arrows to the right and left of the revenue by day chart), **starting from the first month of accounting**. This function is implemented using **Django Paginator**.

**NOTIFICATIONS**: On the notifications page you can find notifications about new employees **who are waiting for log authorization**, if they have not checked the *I'm the owner box* during registration and entered the name of the corresponding game room. *When an employee is authorized*, they are listed as a shared staff member and **have permissions to view the home page and history page, as well as to log new customers and edit the last three days in the log history**.

