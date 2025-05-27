# Platform List

This file includes all platforms considered for the Content Moderation Research Project. 
Each row describes a platform's access link, account creation method, and proposed method(s) of creating a controlled and closed environment.
An exploration of each platform's content moderation systems will also be put in place. 

### Platform Criteria
1. Identifying a method of creating a controlled and private environment for ensuring harmful content not be released for public view.
2. Content Moderation Systems : Whether these platforms utilize keywords based moderation, a combination of automated and human review and other automated tools
3. Extension: Ability to customize and access a platforms AutoMod / Content Moderation Bots as well as the ability to implement plug-ins or API such that our primed and customized LLMs developed can be used for controlled testing. 

### Platform Table
<div>
  <table>
    <tbody>
      <tr>
        <td>
          <span style="color:rgb(31, 35, 40);">
            <strong>Platform</strong>
          </span>
        </td>
        <td>
          <span style="color:rgb(31, 35, 40);">
            <strong>Account Creation</strong>
          </span>
        </td>
        <td>
          <span style="color:rgb(31, 35, 40);">
            <strong>Closed Environment Creation</strong>
          </span>
        </td>
        <td>
          <span style="color:rgb(31, 35, 40);">
            <strong>Pros and Cons</strong>
          </span>
        </td>
        <td>
          <span style="color:rgb(31, 35, 40);">
            <strong>Content Moderation System</strong>
          </span>
        </td>
        <td>
          <span style="color:rgb(31, 35, 40);">
            <strong>Access to LLMs used for Moderation (Allowing Plugins or API)&nbsp;&nbsp;</strong>
          </span>
        </td>
      </tr>
      <tr>
        <td>Youtube</td>
        <td>Via Email + Phone Number required for live streaming</td>
        <td>1. Creating a private stream that is only visible to those emails you provide in the private stream to option.&nbsp;2. Uploading unlisted or private videos which can only be seen by people who have a link or only by the creator.&nbsp;</td>
        <td>Private Stream:&nbsp;- Allows for a much quicker upload and testing cycle- Requires a phone number to be approved to streamPrivate / Unlisted Videos:&nbsp;- More explicit information about it content moderation → options like ‘Is it made for kids’ and Copyright protection- Slower upload and may be too large of a ‘release environment’&nbsp;</td>
        <td>-
          <a target="_blank" href="https://www.youtube.com/howyoutubeworks/policies/community-guidelines/">
            <span style="color:rgb(17, 85, 204);">Community Guidelines</span>
          </a>:&nbsp;Fake Engagement Policy, Hate Speech Policy: ​​<span style="color:rgb(31, 31, 31);">Here are examples of hate speech not allowed on YouTube.</span>
          <span style="color:rgb(31, 31, 31);">
            ---
            -
            -
            -
            -
            -
            -
            -
            ---</span>
          <span style="color:rgb(31, 31, 31);">“I’m glad this [violent event] happened. They got what they deserved [referring to people with protected group status].”</span>
          <span style="color:rgb(31, 31, 31);">“[People with protected group status] are dogs” or “[people with protected group status] are like animals.”</span>
          <span style="color:rgb(31, 31, 31);">
            ---
            -
            -
            -
            -
            -
            -
            -
            ---</span>
          <span style="color:rgb(31, 31, 31);">-
          </span>
          <a target="_blank" href="https://themarkup.org/automated-censorship/2024/03/01/how-automated-content-moderation-works-even-when-it-doesnt-work">
            <span style="color:rgb(17, 85, 204);">How it works</span>
          </a>
          <span style="color:rgb(31, 31, 31);">
            and</span>
          <a target="_blank" href="https://journals.sagepub.com/doi/10.1177/2053951719897945">
            <span style="color:rgb(17, 85, 204);">Paper on Perceptual Hashing for Copyright Policies</span>
          </a>
          <span style="color:rgb(31, 31, 31);">Many diff automated systems scan for patterns / how to treat these patterns that match harmful content from a “Hash Database”&nbsp;</span>
        </td>
        <td>Does not allow for custom LLM or API integration.&nbsp;Rule customization is limited.&nbsp;</td>
      </tr>
      <tr>
        <td>Linkedin</td>
        <td>Via Email&nbsp;</td>
        <td>Private Unlisted Groups on Linkedin allow for just the group owner and invited members to view posts and group content</td>
        <td>- Smaller release environment&nbsp;- Greater controls due to the Group Owner being able to moderate content / identify the Group Rules- It may take a long upload cycle for each post.&nbsp;</td>
        <td>-
          <a target="_blank" href="https://www.linkedin.com/legal/professional-community-policies">
            <span style="color:rgb(17, 85, 204);">Professional Community Guidelines:&nbsp;</span>
          </a>“Be Safe” clause - hate speech and no exploitation of children (specifically)&nbsp;“Be Trustworthy” - Impersonation and misinformation<a target="_blank" href="https://www.linkedin.com/blog/engineering/trust-and-safety/augmenting-our-content-moderation-efforts-through-machine-learni">
            <span style="color:rgb(17, 85, 204);">New framework for reviewing content</span>
          </a>:&nbsp;- Utilizing AI to automate prioritization of content review for human reviewers(interesting)</td>
        <td>Not custom autoMod bot changes or integration with API or LLMs. But can take inspiration from reddit and twitch solutions, we can run scripts for these following platforms that have the ability to customize rules.Extract community rules and feed data into LLMs.&nbsp;&nbsp;Depending on whether we would like the audit to simulate real moderation within the group. Or, after releasing certain content within a platform, our external LLM content mod bot can moderate accordingly.&nbsp;</td>
      </tr>
      <tr>
        <td>Discord</td>
        <td>Via Email</td>
        <td>Creating a
          <a target="_blank" href="https://support.discord.com/hc/en-us/articles/206143407-How-do-I-set-up-a-private-server">
            <span style="color:rgb(17, 85, 204);">private server</span>
          </a>
          with permission for everyone disabled</td>
        <td>- closed environment only between server-leader and members- able to set up different channels for testing each policy- more explicit automated moderator →
          <a target="_blank" href="https://discord.com/safety/auto-moderation-in-discord#:~:text=Built%2Din%20moderation%20features,will%20find%20the%20Moderation%20settings.">
            <span style="color:rgb(17, 85, 204);">AutoMod</span>
          </a>
          for quicker response times on flagging harmful content- Perhaps able to customize reactions of autoMod&nbsp;</td>
        <td>
          <a target="_blank" href="https://discord.com/guidelines">
            <span style="color:rgb(17, 85, 204);">- Community guidelines</span>
          </a>:-
          <a target="_blank" href="https://discord.com/safety/our-approach-to-content-moderation">
            <span style="color:rgb(17, 85, 204);">Approach to Moderation</span>
          </a>:Image hashing and “ML powered tech” for child sexual abuse material+&nbsp;Metadata and network patterns to identify bad actors or spaces with harmful content / activity. (keyword filters)&nbsp;</td>
        <td>^^</td>
      </tr>
      <tr>
        <td>Pinterest</td>
        <td>Email</td>
        <td>Creating a private board of pins (Interesting to look into further.. Removing pins from a board that seem inappropriate via an automated system but aren’t pins public?)&nbsp;</td>
        <td>- things may be secretly flagged as harmful content but not able to see this unless you view with another account – outside the board</td>
        <td>-
          <a target="_blank" href="https://medium.com/pinterest-engineering/how-pinterest-fights-misinformation-hate-speech-and-self-harm-content-with-machine-learning-1806b73b40ef">
            <span style="color:rgb(17, 85, 204);">Content moderation</span>
          </a>
          happens on the level of a pin- grouping similar images together but also on a board level where each board is provided a score&nbsp;</td>
        <td>-</td>
      </tr>
      <tr>
        <td>Facebook</td>
        <td>Email</td>
        <td>Creating a private facebook group.&nbsp;</td>
        <td>- able to manage and test moderation on various mediums within the closed facebook group: Community chats, reels, music, files, and live videos.&nbsp;- distinguish between content that is not allowed and sensitive content&nbsp;</td>
        <td>
          <a target="_blank" href="https://transparency.meta.com/en-gb/policies/community-standards/">
            <span style="color:rgb(17, 85, 204);">Content moderation</span>
          </a>: (Hate speech)&nbsp;- “Generalization that state inferiority (in written or visual form): Physical deficiencies are defined as those about: Hygiene, including, but not limited to: filthy, dirty, smelly or Physical appearance, including, but not limited to: ugly, hideous”- “Animals in general or specific types of animals that are culturally perceived as intellectually or physically inferior (including but not limited to: Black people and apes or ape-like creatures; Jewish people and rats; Muslim people and pigs; Mexican people and worms)”<a target="_blank" href="https://transparency.meta.com/en-gb/enforcement/detecting-violations/how-enforcement-technology-works/">
            <span style="color:rgb(17, 85, 204);">Enforcement</span>
          </a>
          (combination of tech and human review):&nbsp;- Determine if content is under hate speech or violent- Determine action to delete / human reviewIdentifying subtle changes and details in miscommunication - images, item placement or word choice**&nbsp;&nbsp;</td>
        <td>^^</td>
      </tr>
      <tr>
        <td>Github&nbsp;</td>
        <td>Via Email</td>
        <td>Creating a private repository and enabling discussions</td>
        <td>Requires a sort of moderator role in the repo to decide these tasks based on “Community Expectations README file”&nbsp;Does not seem to have built in content moderation systems / automation for public access</td>
        <td>
          <a target="_blank" href="https://github.blog/2021-11-17-githubs-developer-first-approach-to-content-moderation/">
            <span style="color:rgb(17, 85, 204);">Content Moderation approach</span>
          </a>- Using a primed LLM to act as a moderator role (<a target="_blank" href="https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization">
            <span style="color:rgb(17, 85, 204);">Triage or Admin</span>
          </a>)?- Things are often only taken down due to Government or State issues…&nbsp;</td>
        <td>Doesn’t seem to even have a built-in bot for automated content moderation for us to tinker with.&nbsp;No custom moderation other than assigning an actual user.&nbsp;</td>
      </tr>
      <tr>
        <td>Instagram</td>
        <td>Via Email</td>
        <td>Creating a group (like Facebook) that is private - requires a moderator rolePrivate channels for followers on a private profile</td>
        <td>Interesting thought:
          <a target="_blank" href="https://medium.com/acm-cscw/personalizing-content-moderation-on-social-media-sites-f2543e62d2fb">
            <span style="color:rgb(17, 85, 204);">Personalized Content Moderation</span>
          </a>
        </td>
        <td>Very basic and non-detailed description of
          <a target="_blank" href="https://help.instagram.com/423837189385631">
            <span style="color:rgb(17, 85, 204);">AI in content moderation</span>
          </a>:</td>
        <td>Does not provide customizable content moderation:&nbsp;- but could look into external plug-ins where we grab content from Instagram groups / content released in Instagram and use external LLM content mod systems to test against instagram’s moderator.&nbsp;</td>
      </tr>
      <tr>
        <td>
          <strong>Reddit</strong>
        </td>
        <td>Via Email</td>
        <td>Creating a private subreddit&nbsp;</td>
        <td>Seems to have a lot of moderation tools (as named in the moderator column) and more
          <a target="_blank" href="https://support.reddithelp.com/hc/en-us/articles/15484384020756-Moderation-Tools-overview">
            <span style="color:rgb(17, 85, 204);">here</span>
          </a>No immediate access to custom API or LLM access for AutoMod</td>
        <td>Copyright policies:&nbsp;“A person who creates an original work of authorship is protected by copyright law whether or not they register their copyright because copyright protection exists from the moment it’s fixed in a tangible medium of expression.”“We are not responsible for actions taken by the moderators.” “Rule 5 You don’t have to use your real name to use Reddit, but don’t impersonate an individual or an entity in a misleading or deceptive manner.”&nbsp;“Communities and users that incite violence or that promote hate based on identity or vulnerability will be banned.”&nbsp;</td>
        <td>1. Moderation Queue that collates a list of flagged content from users (that could implement same idea of LLM being a user-moderator2. AutoModerator - In-depth moderator documentation about how to set up custom rules - clearly defining actions towards flagged content.&nbsp;- Example: Image hosting from certain ‘common image hosting sites’&nbsp;- Custom keyword searches and defining customized rules that are “automatically applied”&nbsp;Python script with a comments mod via API:
          <a target="_blank" href="https://github.com/conversationai/conversationai-moderator-reddit/tree/main/perspective_reddit_bot">
            <span style="color:rgb(17, 85, 204);">https://github.com/conversationai/conversationai-moderator-reddit/tree/main/perspective_reddit_bot</span>
          </a>
        </td>
      </tr>
      <tr>
        <td>Stackoverflow</td>
        <td>Via Email</td>
        <td>For teams, there is a private channel for discussion that could act as a controlled environment</td>
        <td>Seems to only document a large community of moderators - in fact, a lot of the moderator community is made up of human reviewers and looks more towards the efficiency of code and preciseness of the questions asked&nbsp;</td>
      </tr>
      <tr>
        <td>Tumblr&nbsp;</td>
        <td>Via Email</td>
        <td>
          <a target="_blank" href="https://help.tumblr.com/communities/">
            <span style="color:rgb(17, 85, 204);">Private Community forum - Beta Testing though</span>
          </a>
        </td>
        <td>Many features are still in beta testing so the moderation system may not be well developed if not developed at all.&nbsp;</td>
      </tr>
      <tr>
        <td>
          <strong>Twitch</strong>
        </td>
        <td>VIa Email</td>
        <td>According to one
          <a target="_blank" href="https://www.reddit.com/r/Twitch/comments/finzhw/is_there_an_option_for_privatehidden_streams_on/">
            <span style="color:rgb(17, 85, 204);">user</span>
          </a>: “Make a new account that nobody follows, dont set a game when you go live. If it forces you to, add a bot and try to change the game to something that doesnt exist using a mod command for it. That'll clear the game. You wont show up in any game directories, and only people you give the link to will be able to watch.”</td>
        <td>Allows AutoMods to run in livestream chats and seems to enable custom moderation rules.&nbsp;By using
          <a target="_blank" href="https://github.com/bdougie/git-twitch">
            <span style="color:rgb(17, 85, 204);">this Twitch and Github interaction
            </span>
          </a>tool, we can integrate our own LLM from a git repo - Inspired by this video:
          <a target="_blank" href="https://www.youtube.com/watch?v=yv69xX9_IaI&amp;ab_channel=GitHub">
            <span style="color:rgb(17, 85, 204);">https://www.youtube.com/watch?v=yv69xX9_IaI&amp;ab_channel=GitHub</span>
          </a>
        </td>
        <td>Enabling a user as a ‘human’ moderatorAutoMod that includes ability for customization&nbsp;Chatbots that help further moderation with the chat of a livestream – this may refer to other human reviewers</td>
        <td>Operates the custom autoMod sort of like reddit: Custom keywords section, Category based:&nbsp;Discrimination and Race, religion, gender, etc. Hate speech falls under this category.&nbsp;Sexual Content Words or phrases referring to sexual acts and/or anatomy.&nbsp;Hostility Provocation and bullying.&nbsp;Profanity Expletives, curse words, and vulgarity:&nbsp; This filter especially helps those who wish to keep their community family-friendly.&nbsp;Smart Detection :Detects unwanted messages (including spam) based on mod actions taken in your channel. Currently available in English only.</td>
      </tr>
    </tbody>
  </table>
</div>
